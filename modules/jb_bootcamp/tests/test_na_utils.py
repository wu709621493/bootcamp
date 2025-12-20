"""Tests for nucleic acid utilities."""

import pytest

from jb_bootcamp import base_counts, gc_content


def test_gc_content_mixed_case():
    seq = "AaGgT"
    assert gc_content(seq) == pytest.approx(0.4)


def test_gc_content_allows_uppercase_lowercase():
    seq = "ccGGtt"
    assert gc_content(seq) == pytest.approx(4 / 6)


def test_gc_content_invalid_character():
    with pytest.raises(ValueError):
        gc_content("AGTX")


def test_gc_content_empty_sequence():
    with pytest.raises(ValueError):
        gc_content("")


def test_base_counts_mixed_case_sequence():
    seq = "AaGgTt"
    assert base_counts(seq) == {"A": 2, "T": 2, "G": 2, "C": 0}


def test_base_counts_missing_bases_are_zero():
    seq = "GGTT"
    assert base_counts(seq) == {"A": 0, "T": 2, "G": 2, "C": 0}


def test_base_counts_invalid_character():
    with pytest.raises(ValueError):
        base_counts("AGTX")


def test_base_counts_empty_sequence():
    with pytest.raises(ValueError):
        base_counts("")
