"""Tests for number classification helpers."""

import pytest

from jb_bootcamp.number_utils import abundant_numbers, classify_number, is_perfect_number, proper_divisors


def test_proper_divisors_basic():
    assert proper_divisors(1) == []
    assert proper_divisors(6) == [1, 2, 3]
    assert proper_divisors(28) == [1, 2, 4, 7, 14]


def test_is_perfect_number_and_classification():
    assert is_perfect_number(6)
    assert classify_number(6) == "perfect"
    assert classify_number(12) == "abundant"
    assert classify_number(8) == "deficient"


def test_abundant_numbers_sequence_and_bounds():
    assert abundant_numbers(30) == [12, 18, 20, 24, 30]
    assert abundant_numbers(11) == []


def test_number_validation_errors():
    with pytest.raises(TypeError):
        proper_divisors(2.5)
    with pytest.raises(TypeError):
        classify_number(True)
    with pytest.raises(ValueError):
        abundant_numbers(0)
