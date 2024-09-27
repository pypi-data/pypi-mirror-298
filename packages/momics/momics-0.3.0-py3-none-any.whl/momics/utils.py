from pathlib import Path

import pandas as pd
import pyBigWig
import pyfaidx


def get_chr_lengths(bw: Path) -> dict:
    """Parse bigwig header to extract chromosome lengths

    Args:
        bw (Path): path to a bigwig file

    Returns:
        dict: Dictionary of chromosome lengths
    """
    with pyBigWig.open(bw) as bw:
        a = bw.chroms()
    bw.close()
    return a


def _check_fasta_lengths(fasta, chroms):
    reference_lengths = dict(zip(chroms["chrom"], chroms["length"]))
    with pyfaidx.Fasta(fasta) as fa:
        lengths = {name: len(seq) for name, seq in fa.items()}
    if lengths != reference_lengths:
        raise Exception(f"{fa} file do not have identical chromomosome lengths.")


def _check_chr_lengths(bw_files, chroms):
    reference_lengths = dict(zip(chroms["chrom"], chroms["length"]))
    for file in list(bw_files.values()):
        with pyBigWig.open(file) as bw:
            lengths = bw.chroms()
            if lengths != reference_lengths:
                raise Exception(
                    f"{file} files do not have identical chromomosome lengths."
                )


def _check_track_names(bw_files, tracks):
    labels = set(tracks["label"])
    for element in list(bw_files.keys()):
        if element in labels:
            raise ValueError(
                f"Provided label '{element}' already present in `tracks` table"
            )


def _check_track_name(track, tracks):
    labels = set(tracks["label"])
    if track not in labels:
        raise ValueError(
            f"Provided track name '{track}' does not exist in `tracks` table"
        )


def parse_ucsc_coordinates(coords: str) -> pd.DataFrame:
    """Parse UCSC-style coordinates as a DataFrame

    Args:
        coords (str): A UCSC-style set of coordinates (e.g., "I:11-100"). Note
        that the coordinates are 1-based.

    Returns:
        pd.DataFrame: A pd.DataFrame with at least three columns (`chrom`, `start`, `end`),
        and any other columns stored in the local bed file.
    """
    if isinstance(coords, str):
        coords = [coords]

    chromosomes = []
    starts = []
    ends = []
    for coord in coords:
        try:
            chr_part, range_part = coord.split(":")
            start, end = range_part.split("-")
            start = int(start)
            end = int(end)
            chromosomes.append(chr_part)
            starts.append(start)
            ends.append(end)

        except ValueError:
            return (
                f"Error: Invalid start/end values in coordinate '{coord}'. "
                + "Start and end must be integers."
            )
        except Exception:
            return (
                f"Error: Invalid format for UCSC-style coordinate '{coord}'. "
                + "Expected format: 'chrom:start-end'."
            )

    df = pd.DataFrame({"chrom": chromosomes, "start": starts, "end": ends})

    return df
