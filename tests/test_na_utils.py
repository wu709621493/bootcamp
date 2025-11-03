"""Tests for nucleic-acid helper utilities."""

from pathlib import Path
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import na_utils


def test_rna_transcription_preserves_case():
    """A mixed-case DNA sequence should transcribe correctly."""

    assert na_utils.rna("aCGt") == "acgu"
    assert na_utils.rna("ACGT") == "ACGU"


@pytest.mark.parametrize("sequence", ["ACXT", "No.cancer.wont.die.fly", 123])
def test_rna_validation(sequence):
    """Invalid sequences should raise informative errors."""

    with pytest.raises((TypeError, ValueError)):
        na_utils.rna(sequence)


def test_reverse_rna_complement():
    """The reverse RNA complement should be computed correctly."""

    assert na_utils.reverse_rna_complement("ACGT") == "ACGU"
    assert na_utils.reverse_rna_complement("acgt") == "acgu"
