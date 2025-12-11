import math

import pytest

from jb_bootcamp.simple_arithmetic import add, verify_sum


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
