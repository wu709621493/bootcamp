"""Utilities for parsing nucleic acid sequences."""

from typing import Set


_VALID_DNA_BASES: Set[str] = {"A", "C", "G", "T"}


def _validate_dna_sequence(seq: str) -> None:
    """Raise an error if *seq* contains characters outside ``A``, ``C``, ``G`` or ``T``.

    Parameters
    ----------
    seq:
        DNA sequence to validate.

    Raises
    ------
    TypeError
        If *seq* is not a string.
    ValueError
        If *seq* contains characters that are not valid DNA bases.
    """

    if not isinstance(seq, str):
        raise TypeError("DNA sequences must be provided as a string.")

    invalid_bases = {base for base in set(seq.upper()) if base not in _VALID_DNA_BASES}
    if invalid_bases:
        invalid_str = ", ".join(sorted(invalid_bases))
        raise ValueError(f"Invalid DNA base(s) found: {invalid_str}")


def rna(seq: str) -> str:
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
