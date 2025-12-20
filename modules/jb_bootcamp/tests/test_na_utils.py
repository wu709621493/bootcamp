"""Tests for nucleic acid utilities."""

import pytest

from jb_bootcamp import count_bases, gc_content


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


def test_count_bases_case_insensitive():
    seq = "AaTtGgCc"
    expected_counts = {"A": 2, "T": 2, "G": 2, "C": 2}

    assert count_bases(seq) == expected_counts


def test_count_bases_invalid_character():
    with pytest.raises(ValueError):
        count_bases("AGTN")


def test_count_bases_empty_sequence():
    with pytest.raises(ValueError):
        count_bases("")
