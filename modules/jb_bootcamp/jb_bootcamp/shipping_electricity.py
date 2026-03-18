"""Helpers for estimating shipboard electricity generation.

The module models simple electricity recovery during a voyage, such as waste-
heat recovery or shaft generators that convert propulsion activity into usable
power for onboard systems or export at port.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

__all__ = [
    "ShippingRoute",
    "RouteElectricitySummary",
    "GenerationManifest",
    "estimate_voyage_hours",
    "estimate_generated_electricity",
    "prioritize_routes_by_generation",
    "build_generation_manifest",
]


@dataclass(frozen=True)
class ShippingRoute:
    """Describe a voyage that can recover electricity while underway."""

    name: str
    distance_nm: float
    average_speed_knots: float
    propulsion_power_kw: float
    hotel_load_kw: float = 0.0
    recovery_fraction: float = 0.08

    def __post_init__(self) -> None:  # pragma: no cover - validation is behaviorally exercised
        if not self.name or not self.name.strip():
            raise ValueError("name must be a non-empty string.")
        if self.distance_nm <= 0:
            raise ValueError("distance_nm must be positive.")
        if self.average_speed_knots <= 0:
            raise ValueError("average_speed_knots must be positive.")
        if self.propulsion_power_kw <= 0:
            raise ValueError("propulsion_power_kw must be positive.")
        if self.hotel_load_kw < 0:
            raise ValueError("hotel_load_kw cannot be negative.")
        if not 0.0 <= self.recovery_fraction <= 1.0:
            raise ValueError("recovery_fraction must lie between 0 and 1.")


@dataclass(frozen=True)
class RouteElectricitySummary:
    """Electricity recovery summary for a single route."""

    name: str
    voyage_hours: float
    gross_generation_kwh: float
    net_generation_kwh: float


@dataclass(frozen=True)
class GenerationManifest:
    """Aggregate electricity recovery across multiple routes."""

    total_gross_generation_kwh: float
    total_net_generation_kwh: float
    routes: tuple[RouteElectricitySummary, ...]


def estimate_voyage_hours(
    distance_nm: float,
    *,
    average_speed_knots: float,
    port_turnaround_hours: float = 0.0,
) -> float:
    """Return voyage duration in hours including optional port turnaround."""

    if distance_nm <= 0:
        raise ValueError("distance_nm must be positive.")
    if average_speed_knots <= 0:
        raise ValueError("average_speed_knots must be positive.")
    if port_turnaround_hours < 0:
        raise ValueError("port_turnaround_hours cannot be negative.")

    return distance_nm / average_speed_knots + port_turnaround_hours


def estimate_generated_electricity(
    route: ShippingRoute,
    *,
    port_turnaround_hours: float = 0.0,
    export_efficiency: float = 1.0,
) -> RouteElectricitySummary:
    """Estimate gross and net electricity generated for one shipping route."""

    if port_turnaround_hours < 0:
        raise ValueError("port_turnaround_hours cannot be negative.")
    if not 0.0 <= export_efficiency <= 1.0:
        raise ValueError("export_efficiency must lie between 0 and 1.")

    voyage_hours = estimate_voyage_hours(
        route.distance_nm,
        average_speed_knots=route.average_speed_knots,
        port_turnaround_hours=port_turnaround_hours,
    )
    gross_generation = route.propulsion_power_kw * route.recovery_fraction * voyage_hours
    onboard_consumption = route.hotel_load_kw * voyage_hours
    net_generation = max(0.0, (gross_generation - onboard_consumption) * export_efficiency)

    return RouteElectricitySummary(
        name=route.name.strip(),
        voyage_hours=voyage_hours,
        gross_generation_kwh=gross_generation,
        net_generation_kwh=net_generation,
    )


def prioritize_routes_by_generation(
    routes: Iterable[ShippingRoute],
    *,
    port_turnaround_hours: float = 0.0,
    export_efficiency: float = 1.0,
) -> tuple[RouteElectricitySummary, ...]:
    """Return route summaries sorted by net electricity generation."""

    summaries = [
        estimate_generated_electricity(
            route,
            port_turnaround_hours=port_turnaround_hours,
            export_efficiency=export_efficiency,
        )
        for route in routes
    ]
    summaries.sort(key=lambda summary: (-summary.net_generation_kwh, summary.name))
    return tuple(summaries)


def build_generation_manifest(
    routes: Sequence[ShippingRoute],
    *,
    port_turnaround_hours: float = 0.0,
    export_efficiency: float = 1.0,
) -> GenerationManifest:
    """Build an aggregate manifest of electricity generation across routes."""

    if not routes:
        raise ValueError("routes cannot be empty.")

    summaries = prioritize_routes_by_generation(
        routes,
        port_turnaround_hours=port_turnaround_hours,
        export_efficiency=export_efficiency,
    )
    total_gross = sum(summary.gross_generation_kwh for summary in summaries)
    total_net = sum(summary.net_generation_kwh for summary in summaries)
    return GenerationManifest(
        total_gross_generation_kwh=total_gross,
        total_net_generation_kwh=total_net,
        routes=summaries,
    )
