"""Tests for shipboard electricity generation helpers."""

import math
import pathlib
import sys

import pytest

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from jb_bootcamp.shipping_electricity import (
    GenerationManifest,
    ShippingRoute,
    build_generation_manifest,
    estimate_generated_electricity,
    estimate_voyage_hours,
    prioritize_routes_by_generation,
)


def test_estimate_voyage_hours_includes_port_turnaround():
    result = estimate_voyage_hours(240, average_speed_knots=20, port_turnaround_hours=6)
    assert result == 18


def test_estimate_generated_electricity_accounts_for_hotel_load_and_efficiency():
    route = ShippingRoute(
        name="Pacific Loop",
        distance_nm=300,
        average_speed_knots=25,
        propulsion_power_kw=10_000,
        hotel_load_kw=400,
        recovery_fraction=0.1,
    )

    summary = estimate_generated_electricity(
        route,
        port_turnaround_hours=4,
        export_efficiency=0.9,
    )

    assert math.isclose(summary.voyage_hours, 16)
    assert math.isclose(summary.gross_generation_kwh, 16_000)
    assert math.isclose(summary.net_generation_kwh, (16_000 - 6_400) * 0.9)


def test_prioritize_routes_by_generation_sorts_descending():
    routes = [
        ShippingRoute("Harbor Shuttle", 60, 15, 1_500, hotel_load_kw=150, recovery_fraction=0.06),
        ShippingRoute("Ocean Span", 500, 25, 8_000, hotel_load_kw=300, recovery_fraction=0.08),
        ShippingRoute("Coastal Arc", 180, 18, 4_000, hotel_load_kw=100, recovery_fraction=0.07),
    ]

    summaries = prioritize_routes_by_generation(routes)

    assert [summary.name for summary in summaries] == ["Ocean Span", "Coastal Arc", "Harbor Shuttle"]


def test_build_generation_manifest_aggregates_totals():
    routes = [
        ShippingRoute("North Run", 100, 20, 5_000, hotel_load_kw=200, recovery_fraction=0.08),
        ShippingRoute("South Run", 80, 20, 4_000, hotel_load_kw=100, recovery_fraction=0.05),
    ]

    manifest = build_generation_manifest(routes, port_turnaround_hours=2)

    assert isinstance(manifest, GenerationManifest)
    assert math.isclose(manifest.total_gross_generation_kwh, 4_000)
    assert math.isclose(manifest.total_net_generation_kwh, 2_000)
    assert len(manifest.routes) == 2


@pytest.mark.parametrize(
    "kwargs",
    [
        {"name": "", "distance_nm": 10, "average_speed_knots": 12, "propulsion_power_kw": 1000},
        {"name": "Bad Distance", "distance_nm": 0, "average_speed_knots": 12, "propulsion_power_kw": 1000},
        {"name": "Bad Speed", "distance_nm": 10, "average_speed_knots": -1, "propulsion_power_kw": 1000},
        {"name": "Bad Power", "distance_nm": 10, "average_speed_knots": 12, "propulsion_power_kw": 0},
        {"name": "Bad Hotel", "distance_nm": 10, "average_speed_knots": 12, "propulsion_power_kw": 1000, "hotel_load_kw": -1},
        {"name": "Bad Recovery", "distance_nm": 10, "average_speed_knots": 12, "propulsion_power_kw": 1000, "recovery_fraction": 1.2},
    ],
)
def test_shipping_route_validation(kwargs):
    with pytest.raises(ValueError):
        ShippingRoute(**kwargs)


@pytest.mark.parametrize(
    "func, kwargs",
    [
        (estimate_voyage_hours, {"distance_nm": 0, "average_speed_knots": 20}),
        (estimate_voyage_hours, {"distance_nm": 100, "average_speed_knots": 0}),
        (
            estimate_generated_electricity,
            {
                "route": ShippingRoute("Valid", 100, 20, 2000),
                "export_efficiency": 1.5,
            },
        ),
        (build_generation_manifest, {"routes": []}),
    ],
)
def test_helper_validation(func, kwargs):
    with pytest.raises(ValueError):
        func(**kwargs)
