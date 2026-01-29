"""Utilities for planning egg deliveries."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Iterable, Sequence

__all__ = [
    "EggOrder",
    "OrderSummary",
    "DeliveryManifest",
    "estimate_travel_time",
    "prioritize_orders",
    "build_delivery_manifest",
]


@dataclass(frozen=True)
class EggOrder:
    """Describe an egg order for delivery planning."""

    destination: str
    dozens: int
    distance_km: float
    priority: int = 1

    def __post_init__(self) -> None:  # pragma: no cover - validation covered by behavior tests
        if not self.destination or not self.destination.strip():
            raise ValueError("destination must be a non-empty string.")
        if self.dozens <= 0:
            raise ValueError("dozens must be positive.")
        if self.distance_km <= 0:
            raise ValueError("distance_km must be positive.")
        if self.priority <= 0:
            raise ValueError("priority must be positive.")


@dataclass(frozen=True)
class OrderSummary:
    """Summary of an order's shipping needs."""

    destination: str
    dozens: int
    eggs: int
    crates: int
    travel_time_hr: float


@dataclass(frozen=True)
class DeliveryManifest:
    """Summary of all orders in a delivery run."""

    total_eggs: int
    total_crates: int
    orders: tuple[OrderSummary, ...]


def estimate_travel_time(
    distance_km: float,
    *,
    average_speed_kmh: float = 60.0,
    loading_minutes: float = 20.0,
) -> float:
    """Return the travel time in hours including loading overhead."""

    if distance_km <= 0:
        raise ValueError("distance_km must be positive.")
    if average_speed_kmh <= 0:
        raise ValueError("average_speed_kmh must be positive.")
    if loading_minutes < 0:
        raise ValueError("loading_minutes cannot be negative.")

    return distance_km / average_speed_kmh + loading_minutes / 60.0


def prioritize_orders(orders: Iterable[EggOrder]) -> tuple[EggOrder, ...]:
    """Return orders sorted by priority and distance."""

    return tuple(
        sorted(
            orders,
            key=lambda order: (-order.priority, order.distance_km, order.destination),
        )
    )


def build_delivery_manifest(
    orders: Sequence[EggOrder],
    *,
    eggs_per_dozen: int = 12,
    crate_capacity: int = 180,
    average_speed_kmh: float = 60.0,
    loading_minutes: float = 20.0,
) -> DeliveryManifest:
    """Build a delivery manifest that includes crates and travel times."""

    if not orders:
        raise ValueError("orders cannot be empty.")
    if eggs_per_dozen <= 0:
        raise ValueError("eggs_per_dozen must be positive.")
    if crate_capacity <= 0:
        raise ValueError("crate_capacity must be positive.")

    summaries: list[OrderSummary] = []
    for order in orders:
        eggs = order.dozens * eggs_per_dozen
        crates = ceil(eggs / crate_capacity)
        travel_time = estimate_travel_time(
            order.distance_km,
            average_speed_kmh=average_speed_kmh,
            loading_minutes=loading_minutes,
        )
        summaries.append(
            OrderSummary(
                destination=order.destination,
                dozens=order.dozens,
                eggs=eggs,
                crates=crates,
                travel_time_hr=travel_time,
            )
        )

    total_eggs = sum(summary.eggs for summary in summaries)
    total_crates = sum(summary.crates for summary in summaries)

    return DeliveryManifest(
        total_eggs=total_eggs,
        total_crates=total_crates,
        orders=tuple(summaries),
    )
