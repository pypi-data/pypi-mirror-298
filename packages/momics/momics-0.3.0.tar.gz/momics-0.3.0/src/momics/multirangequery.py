import concurrent.futures

import numpy as np
import pandas as pd
import tiledb
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from .momics import Momics
from .utils import parse_ucsc_coordinates


class MultiRangeQuery:
    """A class to query `.momics` repositories.

    Attributes
    ----------
    momics (Momics): a local `.momics` repository.
    queries (dict): Dict. of pd.DataFrames with at least three columns `chrom`, `start` and `end`, one per chromosome.
    query_labels (list): List of UCSC-style coordinates.
    coverage (dict): Dictionary of coverage scores extracted from the `.momics` repository, populated after calling `q.query_tracks()`
    seq (dict): Dictionary of sequences extracted from the `.momics` repository, populated after calling `q.query_seq()`
    """

    def __init__(self, momics: Momics, bed: pd.DataFrame):
        """Initialize the MultiRangeQuery object.

        Args:
            momics (Momics): a Momics object
            bed (pd.DataFrame): pd.DataFrame with at least three columns `chrom`, `start` and `end`.
        """
        self.momics = momics
        if isinstance(bed, str):
            if ":" in bed:
                bed = parse_ucsc_coordinates(bed)
            else:
                chrom = bed
                chroms = self.momics.chroms()
                chrlength = chroms[chroms["chrom"] == chrom]["length"].iloc[0]
                bed = parse_ucsc_coordinates(f"{chrom}:1-{chrlength}")

        groups = bed.groupby("chrom")
        chrs, indices = np.unique(bed["chrom"], return_index=True)
        sorted_chrs = chrs[np.argsort(indices)]
        queries = {key: group for key, group in groups}
        queries = {key: queries[key] for key in list(sorted_chrs)}
        self.queries = queries
        query_labels = [
            f"{chr}:{start}-{end}"
            for _, (chr, start, end) in enumerate(
                list(zip(bed["chrom"], bed["start"], bed["end"]))
            )
        ]
        self.query_labels = query_labels
        self.coverage = None
        self.seq = None

    def _query_tracks_per_chr(self, chrom, group):

        print(chrom)
        ranges = list(zip(group["start"], group["end"]))

        # Prepare empty long DataFrame without scores, to merge with results
        ranges_str = []
        for _, (start, end) in enumerate(ranges):
            breadth = end - start + 1  # breadth = number of elements in the range
            label = f"{chrom}:{start}-{end}"  # Range1, Range2, Range3, ...
            ranges_str.extend([label] * breadth)  # Repeat the label breadth times
        ranges_df = pd.DataFrame(
            {
                "range": ranges_str,
                "chrom": chrom,
                "position": [
                    item for X in ranges for item in np.arange(X[0], X[1] + 1)
                ],
            }
        )

        # Extract scores from tileDB and wrangle them into DataFrame
        ranges_1 = list(zip(group["start"] - 1, group["end"] - 1))
        tdb = self.momics._build_uri("coverage", f"{chrom}.tdb")
        with tiledb.open(tdb, "r", ctx=self.momics.cfg.ctx) as A:
            subarray = A.multi_index[ranges_1, :]

        # Reformat to add track and range labels
        tr = self.momics.tracks()
        tr = tr[[x != "None" for x in tr["label"]]]
        subarray_df = pd.merge(tr, pd.DataFrame(subarray), on="idx").drop(
            ["idx", "path"], axis=1
        )
        subarray_df["position"] += 1
        df = pd.merge(ranges_df, subarray_df, on="position", how="left")
        res = {}
        for track in list(tr["label"]):
            res[track] = (
                df[df["label"] == track]
                .groupby("range")["scores"]
                .apply(list)
                .to_dict()
            )
        return res

    def _query_seq_per_chr(self, chrom, group):

        print(chrom)
        ranges = list(zip(group["start"], group["end"]))

        # Get sequences
        seqs = {}
        tdb = self.momics._build_uri("genome", "sequence", f"{chrom}.tdb")
        for _, (start, end) in enumerate(ranges):
            with tiledb.open(tdb, "r", ctx=self.momics.cfg.ctx) as A:
                seq = A.df[(start - 1) : (end - 1)]["nucleotide"]
            seqs[f"{chrom}:{start}-{end}"] = "".join(seq)

        return seqs

    def query_tracks(self, threads: int = 1) -> "MultiRangeQuery":
        """Query multiple coverage ranges from a Momics repo.

        Args:
            threads (int, optional): Number of threads for parallel query. Defaults to 1.

        Returns:
            MultiRangeQuery: MultiRangeQuery: An updated MultiRangeQuery object
        """
        ## Process each chr separately
        args = [(chrom, group) for (chrom, group) in self.queries.items()]
        if threads == 1:
            results = [
                self._query_tracks_per_chr(chrom, group) for chrom, group in args
            ]
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                results = list(
                    executor.map(lambda p: self._query_tracks_per_chr(*p), args)
                )

        res = {}
        tr = self.momics.tracks()
        tr = list(tr[[x != "None" for x in tr["label"]]]["label"])
        for track in tr:
            scores_from_all_chrs = [x[track] for x in results]
            d = {k: v for d in scores_from_all_chrs for k, v in d.items()}
            res[track] = {key: d[key] for key in self.query_labels if key in d}

        self.coverage = res
        return self

    def query_sequence(self, threads: int = 1) -> "MultiRangeQuery":
        """Query multiple sequence ranges from a Momics repo.

        Args:
            threads (int, optional): Number of threads for parallel query. Defaults to 1.

        Returns:
            MultiRangeQuery: An updated MultiRangeQuery object
        """
        ## Process each chr separately
        args = [(chrom, group) for (chrom, group) in self.queries.items()]
        if threads == 1:
            seqs = [self._query_seq_per_chr(chrom, group) for chrom, group in args]
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                seqs = list(executor.map(lambda p: self._query_seq_per_chr(*p), args))

        mseqs = {}
        for d in seqs:
            mseqs.update(d)
        self.seq = {"seq": mseqs}
        return self

    def to_df(self) -> pd.DataFrame:
        """Parse self.coverage attribute to a pd.DataFrame

        Returns:
            pd.DataFrame: `self.coverage` dictionary wrangled into a pd.DataFrame
        """
        # Prepare empty long DataFrame without scores, to merge with results
        cov = self.coverage
        if cov is None:
            raise AttributeError(
                "self.coverage is None. Call `self.query_tracks()` to populate it."
            )

        ranges_str = []
        for _, coords in enumerate(self.query_labels):
            chrom, range_part = coords.split(":")
            start = int(range_part.split("-")[0])
            end = int(range_part.split("-")[1])
            label = [
                {"range": coords, "chrom": chrom, "position": x}
                for x in range(start, end + 1)
            ]
            ranges_str.extend(label)
        df = pd.DataFrame(ranges_str)

        for track in list(cov.keys()):
            df[track] = [value for sublist in cov[track].values() for value in sublist]
        return df

    def to_fasta(self) -> SeqRecord:
        """Parse self.seq attribute to a SeqRecord

        Returns:
            SeqRecord: `self.seq` dictionary wrangled into a SeqRecord
        """

        seq = self.seq
        if seq is None:
            raise AttributeError(
                "self.seq is None. Call `self.query_sequence()` to populate it."
            )

        seq_records = []
        for header, sequence in seq["seq"].items():
            seq_record = SeqRecord(Seq(sequence), id=header, description="")
            seq_records.append(seq_record)

        return seq_records
