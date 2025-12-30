import math

import pytest

from jb_bootcamp.vector import Vector


def test_add_and_subtract():
    a = Vector(1, 2, 3)
    b = Vector(4, 5, 6)

    assert a + b == Vector(5, 7, 9)
    assert b - a == Vector(3, 3, 3)


def test_scalar_and_dot_product():
    v = Vector(2, -1)

    assert 3 * v == Vector(6, -3)
    assert v * 0.5 == Vector(1, -0.5)
    assert v * Vector(1, 2) == 0


def test_magnitude_and_normalization():
    v = Vector(3, 4)
    assert math.isclose(v.magnitude, 5)

    unit = v.normalize()
    assert math.isclose(unit.magnitude, 1)
    assert unit == Vector(0.6, 0.8)


def test_distance_requires_matching_dimensions():
    p = Vector(0, 0)
    q = Vector(3, 4)

    assert math.isclose(p.distance_to(q), 5)

    with pytest.raises(ValueError):
        Vector(1, 2, 3).distance_to(Vector(1, 2))


def test_reject_non_numeric_and_empty_vectors():
    with pytest.raises(TypeError):
        Vector(1, "x")

    with pytest.raises(ValueError):
        Vector()
