"""Tests for drilling helpers."""

import math
import pathlib
import sys

import pytest

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from jb_bootcamp.drilling import drill_hole, estimate_spoil_volume


def test_spoil_volume_matches_cylinder_equation():
    depth = 8.0
    diameter = 0.5
    expected = math.pi * (diameter / 2) ** 2 * depth
    assert math.isclose(estimate_spoil_volume(depth, diameter), expected)


def test_drill_hole_reports_duration_and_rate():
    result = drill_hole(
        depth_m=12,
        diameter_m=0.4,
        soil_type="Clay",
        base_penetration_rate_m_per_hr=0.8,
        downtime_fraction=0.1,
    )
    assert math.isclose(result.penetration_rate_m_per_hr, 0.72)
    assert math.isclose(result.duration_hr, 12 / 0.72)
    assert math.isclose(result.spoil_volume_m3, math.pi * (0.2) ** 2 * 12)


def test_drill_hole_rejects_unknown_soil():
    with pytest.raises(KeyError):
        drill_hole(depth_m=5, diameter_m=0.3, soil_type="martian dust")
