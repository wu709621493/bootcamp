"""Tests for nucleic acid utilities."""

import pytest

from jb_bootcamp import gc_content


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
