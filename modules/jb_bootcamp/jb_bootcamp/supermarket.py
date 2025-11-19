"""Operational helpers for running a 超级市场 (supermarket)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import ceil
from typing import Iterable, Mapping, Sequence

__all__ = [
    "SupermarketProduct",
    "Delivery",
    "plan_restock",
    "simulate_inventory",
]


@dataclass(frozen=True)
class SupermarketProduct:
    """Description of a stocked product."""

    name: str
    category: str
    daily_demand: float
    safety_stock: int = 0
    storage: str = "ambient"

    def __post_init__(self) -> None:  # pragma: no cover - fully tested via behaviour
        if not self.name:
            raise ValueError("Products require a non-empty name.")
        if not self.category:
            raise ValueError("Products require a category for reporting.")
        if self.daily_demand <= 0:
            raise ValueError("daily_demand must be positive.")
        if self.safety_stock < 0:
            raise ValueError("safety_stock cannot be negative.")


@dataclass(frozen=True)
class Delivery:
    """Scheduled delivery of inventory."""

    product_name: str
    day: int
    quantity: int

    def __post_init__(self) -> None:  # pragma: no cover - validated in tests
        if self.day < 0:
            raise ValueError("Deliveries cannot occur on negative days.")
        if self.quantity < 0:
            raise ValueError("Delivery quantity must be non-negative.")
        if not self.product_name:
            raise ValueError("Deliveries must reference a product name.")


def plan_restock(
    products: Sequence[SupermarketProduct],
    current_stock: Mapping[str, int],
    *,
    lead_time_days: int,
    planning_days: int,
) -> dict[str, int]:
    """Return purchase quantities needed to stay in stock."""

    if lead_time_days < 0:
        raise ValueError("lead_time_days must be non-negative.")
    if planning_days <= 0:
        raise ValueError("planning_days must be positive.")

    window = lead_time_days + planning_days
    restock: dict[str, int] = {}
    for product in products:
        projected_need = ceil(product.daily_demand * window) + product.safety_stock
        available = max(0, int(current_stock.get(product.name, 0)))
        restock[product.name] = max(0, projected_need - available)
    return restock


def simulate_inventory(
    products: Sequence[SupermarketProduct],
    initial_stock: Mapping[str, int],
    deliveries: Sequence[Delivery],
    demand_pattern: Mapping[str, Sequence[int]],
    *,
    days: int,
) -> dict[str, tuple[int, ...]]:
    """Simulate day-by-day inventory for ``days`` days."""

    if days <= 0:
        raise ValueError("days must be positive.")

    product_names = [product.name for product in products]
    _check_unique(product_names)
    name_set = set(product_names)
    patterns = _normalise_patterns(demand_pattern, name_set)
    schedule = _build_schedule(deliveries, name_set)

    inventory = {name: max(0, int(initial_stock.get(name, 0))) for name in name_set}
    history: dict[str, list[int]] = {name: [] for name in name_set}

    for day in range(days):
        for arrival in schedule.get(day, ()):  # pragma: no branch - depends on data
            inventory[arrival.product_name] += arrival.quantity

        for name in name_set:
            demand = _demand_for_day(patterns.get(name, ()), day)
            sold = min(inventory[name], demand)
            inventory[name] -= sold
            history[name].append(inventory[name])

    return {name: tuple(values) for name, values in history.items()}


def _check_unique(names: Iterable[str]) -> None:
    seen: set[str] = set()
    for name in names:
        if name in seen:
            raise ValueError("Product names must be unique.")
        seen.add(name)


def _normalise_patterns(
    demand_pattern: Mapping[str, Sequence[int]],
    products: set[str],
) -> dict[str, tuple[int, ...]]:
    patterns: dict[str, tuple[int, ...]] = {}
    for name, pattern in demand_pattern.items():
        if name not in products:
            raise KeyError(f"Unknown product in demand pattern: {name}.")
        values = tuple(pattern)
        if not values:
            raise ValueError(f"Demand pattern for {name} cannot be empty.")
        for value in values:
            if value < 0:
                raise ValueError("Demand values must be non-negative.")
        patterns[name] = values
    return patterns


def _build_schedule(
    deliveries: Sequence[Delivery],
    products: set[str],
) -> dict[int, tuple[Delivery, ...]]:
    schedule: dict[int, list[Delivery]] = defaultdict(list)
    for delivery in deliveries:
        if delivery.product_name not in products:
            raise KeyError(f"Unknown product in delivery schedule: {delivery.product_name}.")
        schedule[delivery.day].append(delivery)
    return {day: tuple(entries) for day, entries in schedule.items()}


def _demand_for_day(pattern: Sequence[int], day: int) -> int:
    if not pattern:
        return 0
    return pattern[day % len(pattern)]

