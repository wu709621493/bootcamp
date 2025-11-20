"""Tests for prime utility helpers."""

from jb_bootcamp.prime_utils import armstrong_numbers, is_armstrong_number


def test_is_armstrong_number_truthiness():
    assert is_armstrong_number(0)
    assert is_armstrong_number(1)
    assert is_armstrong_number(153)
    assert not is_armstrong_number(-5)
    assert not is_armstrong_number(10)


def test_armstrong_numbers_range():
    assert armstrong_numbers(500) == [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        153,
        370,
        371,
        407,
    ]
    assert armstrong_numbers(-3) == []
