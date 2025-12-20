import math

import pytest

from jb_bootcamp.simple_arithmetic import add, expo, verify_sum


def test_add_basic_integers():
    assert add(1, 1) == 2


def test_add_preserves_float_and_handles_negative():
    assert math.isclose(add(-2.5, 3.5), 1.0)


def test_add_rejects_non_numeric():
    with pytest.raises(TypeError):
        add("one", 2)


def test_verify_sum_matches_expected():
    assert verify_sum(10, 5, 15) is True


def test_verify_sum_mismatch_raises_value_error():
    with pytest.raises(ValueError):
        verify_sum(1, 1, 3)


def test_expo_handles_non_negative_integer_exponent():
    assert expo(2, 3) == 8
    assert expo(7, 0) == 1


def test_expo_rejects_negative_or_non_integer_exponent():
    with pytest.raises(ValueError):
        expo(2, -1)
    with pytest.raises(TypeError):
        expo(2, 1.5)
