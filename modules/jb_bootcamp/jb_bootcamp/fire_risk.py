"""Wildfire risk assessment helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

__all__ = ["FireObservation", "FireRiskSummary", "compute_fire_risk", "prioritize_fire_risk"]


@dataclass(frozen=True)
class FireObservation:
    """Environmental snapshot used to gauge wildfire risk.

    Parameters
    ----------
    location:
        Human-readable area identifier (e.g. county, ranger district).
    fuel_moisture:
        Fractional fuel moisture content on a ``[0, 1]`` scale where values near
        ``0`` indicate extremely dry vegetation.
    wind_speed:
        Surface wind speed in metres per second.
    relative_humidity:
        Ambient relative humidity as a percentage.
    slope_degrees:
        Terrain slope in degrees; steeper slopes accelerate fire spread.
    recent_lightning_strikes:
        Number of lightning strikes detected in the last 24 hours for the area.
    days_since_rain:
        Days since the last measurable precipitation event.
    """

    location: str
    fuel_moisture: float
    wind_speed: float
    relative_humidity: float
    slope_degrees: float
    recent_lightning_strikes: int = 0
    days_since_rain: int = 0

    def __post_init__(self) -> None:  # pragma: no cover - straightforward validation
        if not isinstance(self.location, str) or not self.location.strip():
            raise ValueError("location must be a non-empty string")
        if not 0.0 <= self.fuel_moisture <= 1.0:
            raise ValueError("fuel_moisture must be between 0 and 1")
        if self.wind_speed < 0:
            raise ValueError("wind_speed must be non-negative")
        if not 0.0 <= self.relative_humidity <= 100.0:
            raise ValueError("relative_humidity must be between 0 and 100")
        if self.slope_degrees < 0:
            raise ValueError("slope_degrees must be non-negative")
        if self.recent_lightning_strikes < 0:
            raise ValueError("recent_lightning_strikes must be non-negative")
        if self.days_since_rain < 0:
            raise ValueError("days_since_rain must be non-negative")


@dataclass(frozen=True)
class FireRiskSummary:
    """Condensed assessment for a single region."""

    location: str
    score: float
    category: str
    recommended_resources: str


def compute_fire_risk(
    observation: FireObservation,
    *,
    dryness_weight: float = 0.35,
    wind_weight: float = 0.25,
    humidity_weight: float = 0.15,
    slope_weight: float = 0.15,
    ignition_weight: float = 0.10,
) -> tuple[float, str]:
    """Return wildfire risk score and category for a single observation.

    Scores are clipped to the ``[0, 1]`` interval and mapped to categories:
    ``extreme`` (>= 0.75), ``high`` (>= 0.55), ``moderate`` (>= 0.35), and
    ``guarded`` (< 0.35).
    """

    total_weight = dryness_weight + wind_weight + humidity_weight + slope_weight + ignition_weight
    if total_weight <= 0:
        raise ValueError("At least one weight must be positive")

    dryness_term = 1.0 - observation.fuel_moisture
    wind_term = min(observation.wind_speed / 20.0, 1.0)
    humidity_term = max(0.0, 1.0 - observation.relative_humidity / 100.0)
    slope_term = min(observation.slope_degrees / 45.0, 1.0)
    lightning_term = min(observation.recent_lightning_strikes / 5.0, 1.0)
    drought_term = min(observation.days_since_rain / 14.0, 1.0)
    ignition_term = 0.5 * (lightning_term + drought_term)

    weighted_score = (
        dryness_weight * dryness_term
        + wind_weight * wind_term
        + humidity_weight * humidity_term
        + slope_weight * slope_term
        + ignition_weight * ignition_term
    ) / total_weight

    score = _clamp_score(weighted_score)
    return score, _category_for_score(score)


def prioritize_fire_risk(
    observations: Sequence[FireObservation],
    *,
    min_score: float = 0.25,
    top_n: int | None = None,
    **weights: float,
) -> tuple[FireRiskSummary, ...]:
    """Generate ranked wildfire risk summaries.

    The optional ``weights`` are forwarded to :func:`compute_fire_risk`, enabling
    bespoke scoring without rewriting ranking logic.
    """

    if not 0.0 <= min_score <= 1.0:
        raise ValueError("min_score must lie in the [0, 1] interval")
    if top_n is not None and top_n <= 0:
        raise ValueError("top_n must be positive when provided")

    summaries = []
    for observation in observations:
        score, category = compute_fire_risk(observation, **weights)
        if score < min_score:
            continue
        summaries.append(
            FireRiskSummary(
                location=observation.location.strip(),
                score=score,
                category=category,
                recommended_resources=_resources_for_category(category),
            )
        )

    summaries.sort(key=lambda summary: summary.score, reverse=True)
    if top_n is not None:
        summaries = summaries[:top_n]
    return tuple(summaries)


def _clamp_score(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


def _category_for_score(score: float) -> str:
    if score >= 0.75:
        return "extreme"
    if score >= 0.55:
        return "high"
    if score >= 0.35:
        return "moderate"
    return "guarded"


def _resources_for_category(category: str) -> str:
    if category == "extreme":
        return "Type 1 incident team, aerial support, structure protection"
    if category == "high":
        return "Hotshot crews, dozers, and retardant drops as needed"
    if category == "moderate":
        return "Initial attack engines with hand crews on standby"
    return "Patrol with lookout coverage"
