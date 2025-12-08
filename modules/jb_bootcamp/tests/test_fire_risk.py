from __future__ import annotations

import pytest

from jb_bootcamp.fire_risk import FireObservation, compute_fire_risk, prioritize_fire_risk


def sample_observations() -> tuple[FireObservation, ...]:
    return (
        FireObservation(
            "Pine Crest",
            fuel_moisture=0.08,
            wind_speed=18.0,
            relative_humidity=15.0,
            slope_degrees=30.0,
            recent_lightning_strikes=3,
            days_since_rain=10,
        ),
        FireObservation(
            "Lake Basin",
            fuel_moisture=0.35,
            wind_speed=6.0,
            relative_humidity=45.0,
            slope_degrees=10.0,
            recent_lightning_strikes=0,
            days_since_rain=3,
        ),
        FireObservation(
            "Foothill Edge",
            fuel_moisture=0.22,
            wind_speed=12.0,
            relative_humidity=25.0,
            slope_degrees=20.0,
            recent_lightning_strikes=1,
            days_since_rain=7,
        ),
    )


def test_compute_fire_risk_categorises_high_threat() -> None:
    observation = FireObservation(
        "Red Canyon",
        fuel_moisture=0.05,
        wind_speed=22.0,
        relative_humidity=10.0,
        slope_degrees=35.0,
        recent_lightning_strikes=4,
        days_since_rain=12,
    )
    score, category = compute_fire_risk(observation)

    assert category == "extreme"
    assert 0.85 <= score <= 1.0


def test_prioritize_fire_risk_orders_and_limits_results() -> None:
    summaries = prioritize_fire_risk(sample_observations(), min_score=0.3, top_n=2)

    assert [summary.location for summary in summaries] == ["Pine Crest", "Foothill Edge"]
    assert summaries[0].category == "extreme"
    assert "Hotshot" in summaries[1].recommended_resources


def test_prioritize_fire_risk_validates_inputs() -> None:
    observations = sample_observations()

    with pytest.raises(ValueError):
        prioritize_fire_risk(observations, min_score=-0.1)
    with pytest.raises(ValueError):
        prioritize_fire_risk(observations, top_n=0)
    with pytest.raises(ValueError):
        compute_fire_risk(observations[0], dryness_weight=0, wind_weight=0, humidity_weight=0, slope_weight=0, ignition_weight=0)
