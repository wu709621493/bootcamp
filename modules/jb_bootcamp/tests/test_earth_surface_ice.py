"""Tests for the earth_surface_ice management helpers."""

from __future__ import annotations

import pytest

from jb_bootcamp.earth_surface_ice import (
    IceField,
    assess_melt_risk,
    plan_interventions,
)


def test_assess_melt_risk_respects_inputs() -> None:
    field = IceField(
        name="Amery",
        area_km2=820.0,
        thickness_m=65.0,
        albedo=0.68,
        ocean_influence=0.25,
    )
    risk = assess_melt_risk(
        field,
        temperature_anomaly=2.1,
        dust_index=0.35,
        solar_radiation=350.0,
    )
    assert risk == pytest.approx(5.5646136, rel=1e-6)

    with pytest.raises(ValueError):
        assess_melt_risk(field, 1.0, dust_index=-0.1)
    with pytest.raises(ValueError):
        assess_melt_risk(field, 1.0, solar_radiation=0.0)


def test_plan_interventions_orders_and_filters() -> None:
    fields = [
        IceField("Aurora", area_km2=1200, thickness_m=70, albedo=0.66, ocean_influence=0.4),
        IceField("Beacon", area_km2=450, thickness_m=35, albedo=0.58, ocean_influence=0.15),
        IceField("Cirrus", area_km2=320, thickness_m=55, albedo=0.72, ocean_influence=0.05),
        IceField("Draco", area_km2=260, thickness_m=25, albedo=0.54, ocean_influence=0.1),
    ]
    anomalies = {"Aurora": 2.8, "Beacon": 1.4, "Cirrus": 0.6, "Draco": 3.3}
    dust = {"Beacon": 0.4, "Draco": 0.2}

    plans = plan_interventions(
        fields,
        anomalies,
        dust_alerts=dust,
        solar_radiation=360.0,
        max_total_area=2200,
        top_n=3,
    )

    assert [plan.name for plan in plans] == ["Draco", "Aurora", "Beacon"]
    assert plans[0].risk_score == pytest.approx(10.0)
    assert plans[1].risk_score >= plans[2].risk_score
    assert plans[0].recommended_action == "deploy brine curtains and shade canopies"
    assert plans[2].recommended_action == "install reflective mesh and dust fences"
    assert plans[1].expected_stability_gain == pytest.approx(0.874, abs=1e-6)

    total_area = sum(plan.area_km2 for plan in plans)
    assert total_area <= 2200


def test_plan_interventions_validates_inputs() -> None:
    fields = [
        IceField("Echo", area_km2=400, thickness_m=40),
        IceField("Echo", area_km2=300, thickness_m=35),
    ]
    anomalies = {"Echo": 1.2}

    with pytest.raises(ValueError):
        plan_interventions(fields, anomalies)

    unique_fields = fields[:1] + [IceField("Fjord", area_km2=200, thickness_m=30)]
    with pytest.raises(KeyError):
        plan_interventions(unique_fields, {"Echo": 1.2})

    with pytest.raises(ValueError):
        plan_interventions(unique_fields, {"Echo": 1.2, "Fjord": 0.3}, top_n=0)
