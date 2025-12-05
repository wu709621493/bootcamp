import pytest

from jb_bootcamp.project_skyline import (
    BuildingPlan,
    ViewCorridor,
    corridor_clearance,
    skyline_outline,
)


def test_skyline_outline_merges_adjacent_blocks():
    plans = [
        BuildingPlan(start=0.0, end=2.0, height=3.0, name="A"),
        BuildingPlan(start=2.0, end=5.0, height=3.0, name="B"),
    ]

    assert skyline_outline(plans) == [(0.0, 3.0), (5.0, 0.0)]


def test_skyline_outline_handles_overlap_and_gaps():
    plans = [
        BuildingPlan(start=0.0, end=3.0, height=2.0),
        BuildingPlan(start=2.0, end=4.0, height=5.0),
        BuildingPlan(start=5.0, end=6.0, height=3.0),
    ]

    outline = skyline_outline(plans)
    assert outline == [
        (0.0, 2.0),
        (2.0, 5.0),
        (4.0, 0.0),
        (5.0, 3.0),
        (6.0, 0.0),
    ]


def test_corridor_clearance_reports_violations():
    plans = [
        BuildingPlan(start=5.0, end=15.0, height=25.0, name="Central Tower"),
        BuildingPlan(start=15.0, end=30.0, height=18.0, name="Harbor Lofts"),
    ]
    corridor = ViewCorridor(origin=0.0, base_height=15.0, slope_per_meter=0.1)

    compliance, violators = corridor_clearance(plans, corridor)

    assert compliance == 0.0
    assert violators == ["Central Tower", "Harbor Lofts"]


def test_corridor_clearance_accepts_compliant_designs():
    plans = [
        BuildingPlan(start=10.0, end=20.0, height=16.0),
        BuildingPlan(start=25.0, end=30.0, height=19.0),
    ]
    corridor = ViewCorridor(origin=0.0, base_height=14.0, slope_per_meter=0.2)

    compliance, violators = corridor_clearance(plans, corridor)

    assert compliance == 1.0
    assert violators == []


def test_corridor_clearance_requires_span():
    empty = []
    corridor = ViewCorridor(origin=0.0, base_height=10.0)

    with pytest.raises(ValueError):
        corridor_clearance(empty, corridor)
