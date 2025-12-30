"""Tests for number classification helpers."""

import pytest

from jb_bootcamp.number_utils import (
    abundant_numbers,
    aliquot_sum,
    comb,
    classify_number,
    is_abundant_number,
    is_perfect_number,
    proper_divisors,
)


def test_proper_divisors_basic():
    assert proper_divisors(1) == []
    assert proper_divisors(6) == [1, 2, 3]
    assert proper_divisors(28) == [1, 2, 4, 7, 14]


def test_is_perfect_number_and_classification():
    assert is_perfect_number(6)
    assert classify_number(6) == "perfect"
    assert classify_number(12) == "abundant"
    assert classify_number(8) == "deficient"


def test_is_abundant_number_checks():
    assert is_abundant_number(12)
    assert not is_abundant_number(6)
    assert not is_abundant_number(11)


def test_aliquot_sum_values():
    assert aliquot_sum(1) == 0
    assert aliquot_sum(6) == 6
    assert aliquot_sum(12) == 16


def test_abundant_numbers_sequence_and_bounds():
    assert abundant_numbers(30) == [12, 18, 20, 24, 30]
    assert abundant_numbers(11) == []


def test_number_validation_errors():
    with pytest.raises(TypeError):
        proper_divisors(2.5)
    with pytest.raises(TypeError):
        classify_number(True)
    with pytest.raises(TypeError):
        aliquot_sum(False)
    with pytest.raises(ValueError):
        abundant_numbers(0)


def test_comb_values_and_validation():
    assert comb(5, 2) == 10
    assert comb(10, 0) == 1
    assert comb(7, 7) == 1
    assert comb(30, 1) == 30

    with pytest.raises(ValueError):
        comb(3, 4)
    with pytest.raises(ValueError):
        comb(-1, 2)
    with pytest.raises(TypeError):
        comb(5.0, 2)
    with pytest.raises(TypeError):
        comb(True, 3)
