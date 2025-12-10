"""Tests for prime utility helpers."""

import subprocess
import sys

import pytest

from jb_bootcamp.prime_utils import (
    armstrong_numbers,
    is_armstrong_number,
    nth_prime,
    prime_factorization,
)


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


def test_prime_factorization_of_composite_number():
    assert prime_factorization(628252) == [2, 2, 17, 9239]


def test_prime_factorization_of_prime_number():
    assert prime_factorization(113) == [113]


def test_prime_factorization_rejects_small_inputs():
    with pytest.raises(ValueError):
        prime_factorization(1)


def test_nth_prime_values_and_validation():
    assert nth_prime(1) == 2
    assert nth_prime(5) == 11
    assert nth_prime(10) == 29
    assert nth_prime(38) == 163

    with pytest.raises(ValueError):
        nth_prime(0)
    with pytest.raises(TypeError):
        nth_prime(2.5)


def test_nth_prime_cli_invocation():
    result = subprocess.run(
        [sys.executable, "-m", "jb_bootcamp.prime_utils", "38"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == "163"
