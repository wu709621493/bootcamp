"""Utilities for ranking Alaska resupply priorities.

The functions here model quick-look logistics scoring for remote Alaska
communities.  The goal is to combine basic readiness indicators—food,
fuel, runway access, and daylight—with real-time storm alerts so that
mission planners can dispatch flights to the highest-risk locations
first.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

__all__ = [
    "AlaskaSite",
    "SitePriority",
    "assess_resupply_gap",
    "prioritize_sites",
]


@dataclass(frozen=True)
class AlaskaSite:
    """Inventory snapshot for a supported site."""

    name: str
    population: int
    fuel_liters: float
    food_days: float
    runway_length_m: float
    daylight_hours: float = 6.0

    def __post_init__(self) -> None:  # pragma: no cover - defensive checks
        if not self.name:
            raise ValueError("name must be provided")
        if self.population <= 0:
            raise ValueError("population must be positive")
        if self.fuel_liters < 0:
            raise ValueError("fuel_liters cannot be negative")
        if self.food_days < 0:
            raise ValueError("food_days cannot be negative")
        if self.runway_length_m <= 0:
            raise ValueError("runway_length_m must be positive")
        if self.daylight_hours < 0:
            raise ValueError("daylight_hours cannot be negative")


@dataclass(frozen=True)
class SitePriority:
    """Priority recommendation for a site."""

    name: str
    priority_score: float
    limiting_factor: str
    recommended_action: str


def assess_resupply_gap(
    site: AlaskaSite,
    *,
    min_food_days: float = 10.0,
    min_fuel_liters_per_person: float = 12.0,
) -> tuple[float, str]:
    """Return a priority score in ``[0, 10]`` and the limiting factor.

    The score compares a site's food and fuel reserves against the
    minimum thresholds while considering runway constraints.  Higher
    values indicate a more urgent need to deliver supplies.
    """

    food_buffer = 1.65 * min_food_days
    food_gap = max(0.0, food_buffer - site.food_days) / max(food_buffer, 1.0)

    fuel_needed = min_fuel_liters_per_person * site.population
    fuel_buffer = 1.5 * fuel_needed
    fuel_gap = max(0.0, fuel_buffer - site.fuel_liters) / max(fuel_buffer, 1.0)

    runway_penalty = 0.0
    if site.runway_length_m < 900.0:
        runway_penalty = (900.0 - site.runway_length_m) / 900.0

    weighted = food_gap * 0.48 + fuel_gap * 0.34 + runway_penalty * 0.28
    severity = food_gap**2 * 0.12 + fuel_gap**2 * 0.1

    score = min((weighted + severity) * 10.0, 10.0)

    if site.runway_length_m < 750.0 or runway_penalty > max(food_gap, fuel_gap):
        limiting_factor = "runway access"
    elif food_gap >= fuel_gap - 0.02:
        limiting_factor = "food"
    else:
        limiting_factor = "fuel"

    return round(score, 2), limiting_factor


def prioritize_sites(
    sites: Sequence[AlaskaSite],
    *,
    storm_risk: Mapping[str, float] | None = None,
    daylight_overrides: Mapping[str, float] | None = None,
    max_sites: int | None = None,
) -> tuple[SitePriority, ...]:
    """Rank sites by combined resupply priority.

    Parameters
    ----------
    sites:
        Sequence of ``AlaskaSite`` entries.
    storm_risk:
        Optional mapping of site name to a ``[0, 1]`` storm likelihood
        multiplier.  Values above one are clamped.
    daylight_overrides:
        Optional mapping for updated daylight hours when recent data are
        available.  Hours are clipped at zero.
    max_sites:
        Maximum number of sites to return once sorted.  If ``None`` all
        sites are returned.
    """

    _validate_unique_names(sites)

    storm_risk = storm_risk or {}
    daylight_overrides = daylight_overrides or {}

    priorities: list[SitePriority] = []
    for site in sites:
        score, limiting = assess_resupply_gap(site)

        risk_multiplier = min(max(storm_risk.get(site.name, 0.0), 0.0), 1.0)
        score *= 1.0 + risk_multiplier * 0.45

        daylight = daylight_overrides.get(site.name, site.daylight_hours)
        daylight = max(daylight, 0.0)
        if daylight < 4.0:
            score *= 1.15
            limiting = f"{limiting} and limited daylight"
        elif daylight < 6.0:
            score *= 1.05

        action = _action_from_score(score, limiting)
        priorities.append(
            SitePriority(
                name=site.name,
                priority_score=round(min(score, 10.0), 2),
                limiting_factor=limiting,
                recommended_action=action,
            )
        )

    priorities.sort(key=lambda entry: (-entry.priority_score, entry.name))
    if max_sites is None:
        return tuple(priorities)
    if max_sites <= 0:
        raise ValueError("max_sites must be positive when provided")
    return tuple(priorities[:max_sites])


def _action_from_score(score: float, limiting: str) -> str:
    if score >= 7.5:
        return "charter heavy-lift cargo with fuel bladders"
    if score >= 5.0:
        return "schedule combined food and diesel drop"
    if "daylight" in limiting:
        return "stage pallets at hub; wait for daylight window"
    return "monitor inventories and coordinate backhaul"


def _validate_unique_names(sites: Sequence[AlaskaSite]) -> None:
    names: set[str] = set()
    for site in sites:
        if site.name in names:
            raise ValueError("site names must be unique")
        names.add(site.name)
