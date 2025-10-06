"""Utilities for parsing nucleic acid sequences."""

from __future__ import annotations

_DNA_BASES = frozenset("ACGTacgt")
_RNA_TRANS = str.maketrans("Tt", "Uu")
_RNA_COMPLEMENT_TRANS = str.maketrans("ACGTacgt", "UGCAugca")


def _normalized_dna(seq: str) -> str:
    """Return *seq* in a consistent case for downstream operations."""

    if seq.isupper():
        return seq.upper()
    return seq.lower()


def _validate_dna(seq: str) -> None:
    """Ensure *seq* contains only canonical DNA bases."""

    invalid = set(seq) - _DNA_BASES
    if invalid:
        invalid_chars = "', '".join(sorted(invalid))
        raise ValueError(
            f"Sequence contains invalid DNA characters: '{invalid_chars}'."
        )


def dna_to_rna(seq: str) -> str:
    """Convert a DNA sequence to RNA.

    Parameters
    ----------
    seq
        DNA sequence consisting solely of the characters ``A``, ``C``, ``G``,
        and ``T`` (case-insensitive).

    Returns
    -------
    str
        RNA sequence where thymine is replaced by uracil. Mixed-case input is
        normalised to lower case to mirror the historical behaviour of this
        function.

    Raises
    ------
    ValueError
        If *seq* contains characters other than canonical DNA bases.
    """

    _validate_dna(seq)
    normalized = _normalized_dna(seq)
    return normalized.translate(_RNA_TRANS)


def reverse_rna_complement(seq: str) -> str:
    """Convert a DNA sequence into its reverse complement as RNA.

    Parameters
    ----------
    seq
        DNA sequence consisting solely of the characters ``A``, ``C``, ``G``,
        and ``T`` (case-insensitive).

    Returns
    -------
    str
        Reverse complement of *seq* expressed as RNA.

    Raises
    ------
    ValueError
        If *seq* contains characters other than canonical DNA bases.
    """

    _validate_dna(seq)
    normalized = _normalized_dna(seq)
    reversed_seq = normalized[::-1]
    return reversed_seq.translate(_RNA_COMPLEMENT_TRANS)
