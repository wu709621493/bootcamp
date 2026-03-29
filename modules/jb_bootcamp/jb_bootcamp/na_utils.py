"""Utilities for parsing nucleic acid sequences."""

from typing import Set


_VALID_DNA_BASES: Set[str] = {"A", "C", "G", "T"}


def _validate_dna_sequence(seq: str) -> None:
    """Validate that *seq* contains only canonical DNA bases."""

    if not isinstance(seq, str):
        raise TypeError("DNA sequences must be provided as a string.")

    invalid_bases = {base for base in set(seq.upper()) if base not in _VALID_DNA_BASES}
    if invalid_bases:
        invalid_str = ", ".join(sorted(invalid_bases))
        raise ValueError(f"Invalid DNA base(s) found: {invalid_str}")


def dna_to_rna(seq: str) -> str:
    """Convert a DNA sequence to RNA after validating the input."""

    _validate_dna_sequence(seq)

    # Determine if original sequence was uppercase
    seq_upper = seq.isupper()

    # Convert to lowercase
    seq = seq.lower()

    # Swap out 't' for 'u'
    seq = seq.replace('t', 'u')

    # Return upper or lower case RNA sequence
    if seq_upper:
        return seq.upper()
    else:
        return seq


def reverse_rna_complement(seq: str) -> str:
    """Convert a DNA sequence into its reverse complement as RNA."""

    _validate_dna_sequence(seq)

    # Determine if original was uppercase
    seq_upper = seq.isupper()

    # Reverse sequence
    seq = seq[::-1]

    # Convert to upper
    seq = seq.upper()

    # Compute complement
    seq = seq.replace('A', 'u')
    seq = seq.replace('T', 'a')
    seq = seq.replace('G', 'c')
    seq = seq.replace('C', 'g')

    # Return result
    if seq_upper:
        return seq.upper()
    else:
        return seq


def gc_content(seq):
    """
    Compute the fraction of bases in a DNA sequence that are G or C.

    Parameters
    ----------
    seq : str
        DNA sequence consisting of A, T, G, and C characters.

    Returns
    -------
    float
        Fraction of characters that are either G or C.

    Raises
    ------
    ValueError
        If the sequence is empty or contains invalid characters.
    """

    if not seq:
        raise ValueError("Sequence must not be empty.")

    seq_upper = seq.upper()
    valid_bases = {"A", "T", "G", "C"}
    invalid_bases = set(seq_upper) - valid_bases

    if invalid_bases:
        invalid_str = "".join(sorted(invalid_bases))
        raise ValueError(f"Invalid nucleotides present: {invalid_str}")

    gc_count = sum(base in {"G", "C"} for base in seq_upper)
    return gc_count / len(seq_upper)


def base_counts(seq):
    """
    Count the number of A, T, G, and C bases in a DNA sequence.

    Parameters
    ----------
    seq : str
        DNA sequence consisting of A, T, G, and C characters.

    Returns
    -------
    dict
        Dictionary mapping uppercase nucleotide characters (A, T, G, C) to
        their respective counts. Bases not present in the sequence have a
        count of zero.

    Raises
    ------
    ValueError
        If the sequence is empty or contains invalid characters.
    """

    if not seq:
        raise ValueError("Sequence must not be empty.")

    seq_upper = seq.upper()
    valid_bases = {"A", "T", "G", "C"}
    invalid_bases = set(seq_upper) - valid_bases

    if invalid_bases:
        invalid_str = "".join(sorted(invalid_bases))
        raise ValueError(f"Invalid nucleotides present: {invalid_str}")

    counts = {base: 0 for base in valid_bases}

    for base in seq_upper:
        counts[base] += 1

    return counts
