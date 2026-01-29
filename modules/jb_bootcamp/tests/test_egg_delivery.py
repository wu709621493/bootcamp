"""Tests for egg delivery helpers."""

import pathlib
import sys

import pytest

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from jb_bootcamp.egg_delivery import (
    EggOrder,
    build_delivery_manifest,
    estimate_travel_time,
    prioritize_orders,
)


def test_estimate_travel_time_includes_loading():
    assert estimate_travel_time(120, average_speed_kmh=60, loading_minutes=30) == 2.5


def test_build_delivery_manifest_sums_eggs_and_crates():
    orders = [
        EggOrder(destination="Cedar Market", dozens=10, distance_km=45),
        EggOrder(destination="Elm Bakery", dozens=5, distance_km=30),
    ]

    manifest = build_delivery_manifest(orders, crate_capacity=120)

    assert manifest.total_eggs == 180
    assert manifest.total_crates == 2
    assert manifest.orders[0].crates == 1
    assert manifest.orders[1].eggs == 60


def test_prioritize_orders_sorts_by_priority_then_distance():
    orders = [
        EggOrder(destination="West", dozens=4, distance_km=15, priority=2),
        EggOrder(destination="East", dozens=4, distance_km=10, priority=2),
        EggOrder(destination="North", dozens=4, distance_km=8, priority=3),
    ]

    sorted_orders = prioritize_orders(orders)

    assert [order.destination for order in sorted_orders] == ["North", "East", "West"]


def test_build_delivery_manifest_rejects_empty_orders():
    with pytest.raises(ValueError):
        build_delivery_manifest([])
