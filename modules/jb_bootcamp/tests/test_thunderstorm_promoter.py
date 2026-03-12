from __future__ import annotations

import pytest

from jb_bootcamp.thunderstorm_promoter import (
    ThunderstormSignal,
    build_promotion_plan,
    severity_score,
)


def test_severity_score_reaches_critical_ranges() -> None:
    signal = ThunderstormSignal(
        area="Metro Core",
        lightning_strikes_per_hour=32,
        rainfall_mm_per_hour=28,
        wind_gust_kmh=90,
        population_density_index=0.95,
        outdoor_event_attendance=18000,
    )

    score = severity_score(signal)

    assert 0.75 <= score <= 1.0


def test_build_promotion_plan_prioritizes_and_limits() -> None:
    signals = (
        ThunderstormSignal("Harbor", 12, 22, 65, 0.7, 8000),
        ThunderstormSignal("Hilltown", 7, 10, 35, 0.3, 300),
        ThunderstormSignal("Metro Core", 30, 34, 95, 0.95, 14000),
    )

    plans = build_promotion_plan(signals, min_severity=0.35, top_n=2)

    assert [plan.area for plan in plans] == ["Metro Core", "Harbor"]
    assert plans[0].priority == "critical"
    assert "social" in plans[1].channel


def test_build_promotion_plan_validates_thresholds() -> None:
    sample = (ThunderstormSignal("Park", 1, 2, 10, 0.2, 0),)

    with pytest.raises(ValueError):
        build_promotion_plan(sample, min_severity=-0.1)

    with pytest.raises(ValueError):
        build_promotion_plan(sample, top_n=0)
