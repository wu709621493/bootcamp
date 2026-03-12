"""Thunderstorm preparedness promotion helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

__all__ = [
    "ThunderstormSignal",
    "PromotionPlan",
    "severity_score",
    "build_promotion_plan",
]


@dataclass(frozen=True)
class ThunderstormSignal:
    """Observed weather and audience factors for a local area."""

    area: str
    lightning_strikes_per_hour: float
    rainfall_mm_per_hour: float
    wind_gust_kmh: float
    population_density_index: float
    outdoor_event_attendance: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.area, str) or not self.area.strip():
            raise ValueError("area must be a non-empty string")
        if self.lightning_strikes_per_hour < 0:
            raise ValueError("lightning_strikes_per_hour must be non-negative")
        if self.rainfall_mm_per_hour < 0:
            raise ValueError("rainfall_mm_per_hour must be non-negative")
        if self.wind_gust_kmh < 0:
            raise ValueError("wind_gust_kmh must be non-negative")
        if not 0.0 <= self.population_density_index <= 1.0:
            raise ValueError("population_density_index must be between 0 and 1")
        if self.outdoor_event_attendance < 0:
            raise ValueError("outdoor_event_attendance must be non-negative")


@dataclass(frozen=True)
class PromotionPlan:
    """Preparedness outreach recommendation for one area."""

    area: str
    severity: float
    priority: str
    channel: str
    message: str


def severity_score(signal: ThunderstormSignal) -> float:
    """Compute a normalized ``[0, 1]`` severity estimate."""

    lightning = min(signal.lightning_strikes_per_hour / 30.0, 1.0)
    rainfall = min(signal.rainfall_mm_per_hour / 40.0, 1.0)
    wind = min(signal.wind_gust_kmh / 100.0, 1.0)
    crowd = min(signal.outdoor_event_attendance / 15000.0, 1.0)

    score = (
        0.35 * lightning
        + 0.25 * rainfall
        + 0.2 * wind
        + 0.1 * signal.population_density_index
        + 0.1 * crowd
    )
    return min(max(score, 0.0), 1.0)


def build_promotion_plan(
    signals: Sequence[ThunderstormSignal],
    *,
    min_severity: float = 0.3,
    top_n: int | None = None,
) -> tuple[PromotionPlan, ...]:
    """Return prioritized thunderstorm safety campaigns for affected areas."""

    if not 0.0 <= min_severity <= 1.0:
        raise ValueError("min_severity must be between 0 and 1")
    if top_n is not None and top_n <= 0:
        raise ValueError("top_n must be positive when provided")

    plans = []
    for signal in signals:
        severity = severity_score(signal)
        if severity < min_severity:
            continue
        priority = _priority_for_severity(severity)
        channel = _channel_for_priority(priority)
        plans.append(
            PromotionPlan(
                area=signal.area.strip(),
                severity=severity,
                priority=priority,
                channel=channel,
                message=_message_for_priority(priority),
            )
        )

    plans.sort(key=lambda plan: plan.severity, reverse=True)
    if top_n is not None:
        plans = plans[:top_n]
    return tuple(plans)


def _priority_for_severity(severity: float) -> str:
    if severity >= 0.75:
        return "critical"
    if severity >= 0.55:
        return "high"
    if severity >= 0.35:
        return "elevated"
    return "watch"


def _channel_for_priority(priority: str) -> str:
    if priority == "critical":
        return "cell broadcast + radio interruption"
    if priority == "high":
        return "sms alert + social amplification"
    if priority == "elevated":
        return "social posts + transit signage"
    return "community bulletin"


def _message_for_priority(priority: str) -> str:
    if priority == "critical":
        return "Move indoors now, avoid windows, and pause all outdoor activity."
    if priority == "high":
        return "Shelter plans should activate; postpone field and rooftop work."
    if priority == "elevated":
        return "Monitor weather updates and secure loose outdoor equipment."
    return "Thunderstorm risk is low but remain weather-aware."
