from __future__ import annotations

import pytest

from jb_bootcamp.war_zone_commerce_model import CommerceSignal, model_war_zone_commerce


def sample_signals() -> tuple[CommerceSignal, ...]:
    return (
        CommerceSignal(
            "North Corridor",
            security_score=0.8,
            supply_route_integrity=0.7,
            market_access=0.75,
            currency_stability=0.65,
            aid_dependency=0.2,
        ),
        CommerceSignal(
            "North Corridor",
            security_score=0.7,
            supply_route_integrity=0.6,
            market_access=0.7,
            currency_stability=0.6,
            aid_dependency=0.25,
        ),
        CommerceSignal(
            "South Basin",
            security_score=0.4,
            supply_route_integrity=0.35,
            market_access=0.45,
            currency_stability=0.3,
            aid_dependency=0.5,
        ),
    )


def test_model_war_zone_commerce_ranks_regions() -> None:
    assessments = model_war_zone_commerce(sample_signals())

    assert [a.region for a in assessments] == ["North Corridor", "South Basin"]
    assert assessments[0].commerce_state == "fragile"
    assert assessments[0].viability_score == pytest.approx(0.680, rel=1e-3)
    assert assessments[0].signal_count == 2

    assert assessments[1].commerce_state == "collapsed"
    assert assessments[1].viability_score == pytest.approx(0.336, rel=1e-3)


def test_model_war_zone_commerce_filters_by_min_viability() -> None:
    assessments = model_war_zone_commerce(sample_signals(), min_viability=0.5)
    assert len(assessments) == 1
    assert assessments[0].region == "North Corridor"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"min_viability": -0.1},
        {"min_viability": 1.1},
        {
            "security_weight": 0.0,
            "logistics_weight": 0.0,
            "access_weight": 0.0,
            "currency_weight": 0.0,
        },
        {"aid_penalty_weight": -0.1},
    ],
)
def test_model_war_zone_commerce_parameter_validation(kwargs: dict[str, float]) -> None:
    with pytest.raises(ValueError):
        model_war_zone_commerce(sample_signals(), **kwargs)


def test_commerce_signal_validation() -> None:
    with pytest.raises(ValueError):
        CommerceSignal(
            "",
            security_score=0.5,
            supply_route_integrity=0.5,
            market_access=0.5,
            currency_stability=0.5,
        )

    with pytest.raises(ValueError):
        CommerceSignal(
            "Region",
            security_score=1.2,
            supply_route_integrity=0.5,
            market_access=0.5,
            currency_stability=0.5,
        )
