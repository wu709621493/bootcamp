"""Tests for :mod:`jb_bootcamp.vehicle_energy`."""

from __future__ import annotations

import pytest

from jb_bootcamp.vehicle_energy import (
    DEFAULT_VEHICLE_PROFILES,
    build_vehicle_energy_chart,
    parse_vehicle_energy_spec,
    VehicleEnergyProfile,
)


def test_parse_vehicle_energy_spec_returns_expected_structure() -> None:
    spec = (
        "mopad -> motorcycle -> 4-wheel-drive -> .space-vessel. -> "
        "energy.chart.localization.=propelant.type.ecological.impact.epact.dat.fly"
    )

    parsed = parse_vehicle_energy_spec(spec)

    assert parsed["vehicle_chain"] == [
        "mopad",
        "motorcycle",
        "4-wheel-drive",
        "space-vessel",
    ]
    assert parsed["chart_assignment"] == {
        "chart_path": ("energy", "chart", "localization"),
        "attribute_path": (
            "propelant",
            "type",
            "ecological",
            "impact",
            "epact",
            "dat",
            "fly",
        ),
    }


@pytest.mark.parametrize(
    "spec",
    [
        "",
        "-> ->",
        " energy.chart.localization.=propellant",
        "mopad",
        "mopad-> chart=",
        "mopad->chart.one=alpha->beta.gamma=delta",
    ],
)
def test_parse_vehicle_energy_spec_rejects_invalid_input(spec: str) -> None:
    with pytest.raises(ValueError):
        parse_vehicle_energy_spec(spec)


def test_build_vehicle_energy_chart_uses_default_profiles() -> None:
    spec = (
        "mopad->motorcycle->4-wheel-drive->space-vessel->"
        "energy.chart.localization.=propelant.type.ecological.impact"
    )

    chart = build_vehicle_energy_chart(spec)

    names = [profile["name"] for profile in chart["profiles"]]
    assert names == ["moped", "motorcycle", "4-wheel drive", "space vessel"]


def test_build_vehicle_energy_chart_falls_back_to_close_match() -> None:
    custom_profiles = {
        "hover-cycle": VehicleEnergyProfile(
            name="hover cycle",
            propellant_type="ion drive",
            ecological_impact="unknown",
            notes="Futuristic transportation prototype.",
        )
    }

    spec = (
        "hover-cycles->energy.chart.localization.=propelant.type.ecological.impact"
    )

    chart = build_vehicle_energy_chart(spec, profiles=custom_profiles)

    assert chart["profiles"][0]["name"] == "hover cycle"


def test_build_vehicle_energy_chart_generates_placeholder_profile() -> None:
    spec = (
        "unknown-speeder->energy.chart.localization.=propelant.type.ecological.impact"
    )

    chart = build_vehicle_energy_chart(spec, profiles=DEFAULT_VEHICLE_PROFILES)

    placeholder = chart["profiles"][0]
    assert placeholder["propellant_type"] == "unknown"
    assert placeholder["name"] == "unknown speeder"
