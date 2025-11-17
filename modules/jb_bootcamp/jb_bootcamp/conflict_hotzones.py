"""Utilities for aggregating conflict reports into war hot zone markers."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Sequence

__all__ = ["ConflictEvent", "WarHotZone", "mark_war_hot_zones"]


@dataclass(frozen=True)
class ConflictEvent:
    """A single conflict observation contributing to hot zone analysis.

    Parameters
    ----------
    region:
        Human-readable region identifier (e.g. province, corridor name).
    intensity:
        Normalised indicator for fighting intensity.  Values are interpreted on
        a ``[0, 10]`` scale but only the non-negativity requirement is enforced.
    displacement:
        Estimated population displacement produced by the event.
    infrastructure_disruption:
        Fractional measure of infrastructure disruption on a ``[0, 1]`` scale.
    days_since_report:
        Age of the report in days. ``0`` indicates an event in the current
        reporting cycle.
    """

    region: str
    intensity: float
    displacement: int = 0
    infrastructure_disruption: float = 0.0
    days_since_report: int = 0

    def __post_init__(self) -> None:  # pragma: no cover - trivial validation
        if not isinstance(self.region, str) or not self.region.strip():
            raise ValueError("region must be a non-empty string")
        if self.intensity < 0:
            raise ValueError("intensity must be non-negative")
        if self.displacement < 0:
            raise ValueError("displacement must be non-negative")
        if not 0.0 <= self.infrastructure_disruption <= 1.0:
            raise ValueError("infrastructure_disruption must be between 0 and 1")
        if self.days_since_report < 0:
            raise ValueError("days_since_report must be non-negative")


@dataclass(frozen=True)
class WarHotZone:
    """Summary describing a region flagged as a war hot zone."""

    region: str
    score: float
    level: str
    event_count: int
    total_intensity: float
    displaced_population: int


def mark_war_hot_zones(
    events: Sequence[ConflictEvent],
    *,
    severity_weight: float = 0.5,
    displacement_weight: float = 0.3,
    infrastructure_weight: float = 0.2,
    recency_half_life_days: float = 21.0,
    min_score: float = 0.5,
    top_n: int | None = None,
) -> tuple[WarHotZone, ...]:
    """Identify the hottest conflict regions from ``events``.

    Scores are computed by summing recency-weighted contributions across all
    events belonging to the same region.  The combined score is capped at ``1``
    and used to assign an alert level:

    ``critical`` (>= 0.85), ``severe`` (>= 0.65), ``elevated`` (< 0.65).
    """

    if not 0.0 <= min_score <= 1.0:
        raise ValueError("min_score must lie in the [0, 1] interval")
    if top_n is not None and top_n <= 0:
        raise ValueError("top_n must be positive when provided")
    if recency_half_life_days <= 0:
        raise ValueError("recency_half_life_days must be positive")

    total_weight = severity_weight + displacement_weight + infrastructure_weight
    if total_weight <= 0:
        raise ValueError("At least one weight must be positive")

    aggregates: Dict[str, Dict[str, float]] = {}
    for event in events:
        region = event.region.strip()
        bucket = aggregates.setdefault(
            region,
            {
                "score": 0.0,
                "count": 0.0,
                "intensity": 0.0,
                "displaced": 0.0,
            },
        )
        bucket["score"] += _event_contribution(
            event,
            severity_weight,
            displacement_weight,
            infrastructure_weight,
            total_weight,
            recency_half_life_days,
        )
        bucket["count"] += 1
        bucket["intensity"] += event.intensity
        bucket["displaced"] += event.displacement

    zones = [
        WarHotZone(
            region=region,
            score=_clamp_score(data["score"]),
            level=_level_for_score(_clamp_score(data["score"])),
            event_count=int(data["count"]),
            total_intensity=data["intensity"],
            displaced_population=int(data["displaced"]),
        )
        for region, data in aggregates.items()
        if _clamp_score(data["score"]) >= min_score
    ]

    zones.sort(key=lambda zone: zone.score, reverse=True)
    if top_n is not None:
        zones = zones[:top_n]
    return tuple(zones)


def _event_contribution(
    event: ConflictEvent,
    severity_weight: float,
    displacement_weight: float,
    infrastructure_weight: float,
    total_weight: float,
    recency_half_life_days: float,
) -> float:
    recency_factor = math.exp(-event.days_since_report / recency_half_life_days)
    severity_term = min(event.intensity / 10.0, 1.0)
    displacement_term = min(event.displacement / 50_000.0, 1.0)
    infrastructure_term = event.infrastructure_disruption

    weighted = (
        severity_weight * severity_term
        + displacement_weight * displacement_term
        + infrastructure_weight * infrastructure_term
    ) / total_weight
    return recency_factor * weighted


def _clamp_score(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


def _level_for_score(score: float) -> str:
    if score >= 0.85:
        return "critical"
    if score >= 0.65:
        return "severe"
    return "elevated"
