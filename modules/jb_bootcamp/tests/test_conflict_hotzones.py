from __future__ import annotations

import pytest

from jb_bootcamp.conflict_hotzones import ConflictEvent, mark_war_hot_zones


def sample_events() -> tuple[ConflictEvent, ...]:
    return (
        ConflictEvent(
            "Verdant Front",
            intensity=8.5,
            displacement=15_000,
            infrastructure_disruption=0.6,
            days_since_report=1,
        ),
        ConflictEvent(
            "Verdant Front",
            intensity=6.0,
            displacement=7_000,
            infrastructure_disruption=0.4,
            days_since_report=5,
        ),
        ConflictEvent(
            "Harbor Shield",
            intensity=4.0,
            displacement=5_000,
            infrastructure_disruption=0.2,
            days_since_report=10,
        ),
        ConflictEvent(
            "Harbor Shield",
            intensity=3.0,
            displacement=3_000,
            infrastructure_disruption=0.1,
            days_since_report=3,
        ),
        ConflictEvent(
            "Mesa Line",
            intensity=2.0,
            displacement=1_000,
            infrastructure_disruption=0.05,
            days_since_report=30,
        ),
    )


def test_mark_war_hot_zones_highlights_regions() -> None:
    zones = mark_war_hot_zones(sample_events(), min_score=0.3)
    assert [zone.region for zone in zones] == ["Verdant Front", "Harbor Shield"]
    assert zones[0].level == "critical"
    assert zones[0].score == pytest.approx(0.938, rel=1e-3)
    assert zones[0].event_count == 2
    assert zones[0].displaced_population == 22_000


def test_mark_war_hot_zones_respects_limits() -> None:
    zones = mark_war_hot_zones(sample_events(), min_score=0.0, top_n=1)
    assert len(zones) == 1
    assert zones[0].region == "Verdant Front"


@pytest.mark.parametrize(
    "params, error",
    [
        ({"min_score": -0.1}, ValueError),
        ({"min_score": 1.5}, ValueError),
        ({"top_n": 0}, ValueError),
        ({"recency_half_life_days": 0}, ValueError),
        (
            {
                "severity_weight": 0.0,
                "displacement_weight": 0.0,
                "infrastructure_weight": 0.0,
            },
            ValueError,
        ),
    ],
)
def test_mark_war_hot_zones_validates_parameters(params: dict, error: type[Exception]) -> None:
    with pytest.raises(error):
        mark_war_hot_zones(sample_events(), **params)
