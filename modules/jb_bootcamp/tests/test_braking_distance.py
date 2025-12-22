import math

import pytest

from jb_bootcamp.rocket_landing import braking_distance


def test_braking_distance_basic():
    distance = braking_distance(20.0, available_upward_acceleration=10.0, buffer=5.0)
    assert math.isclose(distance, 20.0 ** 2 / (2 * 10.0) + 5.0)


def test_braking_distance_zero_descent_speed():
    assert braking_distance(0.0, available_upward_acceleration=15.0, buffer=2.5) == 2.5


def test_braking_distance_validation():
    with pytest.raises(ValueError):
        braking_distance(-1.0, available_upward_acceleration=10.0)
    with pytest.raises(ValueError):
        braking_distance(5.0, available_upward_acceleration=0.0)
    with pytest.raises(ValueError):
        braking_distance(5.0, available_upward_acceleration=-3.0)
    with pytest.raises(ValueError):
        braking_distance(1.0, available_upward_acceleration=5.0, buffer=-0.1)
