"""Tests for symmetry-aware dimensionality reduction utilities."""

import math

import pytest

from jb_bootcamp.symmetry_reduction import (
    analyze_complex_symmetry,
    analyze_fly_landscape,
    project_landscape,
)


def test_fly_landscape_has_asymmetric_axis_ratio():
    result = analyze_fly_landscape(40)
    leading, trailing = result.principal_axes
    assert leading.eigenvalue >= trailing.eigenvalue
    assert result.axis_ratio > 1.0
    for axis in result.principal_axes:
        vx, vy = axis.direction
        assert math.isclose(math.hypot(vx, vy), 1.0, rel_tol=1e-9)


def test_project_landscape_matches_axis_direction():
    sequence = [complex(float(n), 2.0 * float(n)) for n in range(1, 5)]
    result = analyze_complex_symmetry(sequence)
    projections = project_landscape(sequence, result.principal_axes)
    assert projections == pytest.approx([math.hypot(1, 2) * n for n in range(1, 5)])


def test_nearly_circular_sequence_is_symmetric():
    sequence = [complex(math.cos(theta), math.sin(theta)) for theta in [0, math.pi / 2, math.pi, 3 * math.pi / 2]]
    result = analyze_complex_symmetry(sequence)
    assert math.isclose(result.axis_ratio, 1.0, rel_tol=1e-6, abs_tol=1e-6)


def test_requires_multiple_points():
    with pytest.raises(ValueError):
        analyze_complex_symmetry([complex(0.0, 0.0)])
    with pytest.raises(ValueError):
        analyze_fly_landscape(1)

