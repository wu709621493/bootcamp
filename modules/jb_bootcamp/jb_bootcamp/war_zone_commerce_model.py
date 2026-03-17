"""Modeling utilities for estimating commerce viability in war zones."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence

__all__ = [
    "CommerceSignal",
    "WarZoneCommerceAssessment",
    "model_war_zone_commerce",
]


@dataclass(frozen=True)
class CommerceSignal:
    """Single observation used to estimate commerce viability in a region.

    Parameters
    ----------
    region:
        Human-readable region identifier.
    security_score:
        Security indicator on a ``[0, 1]`` scale, where higher is safer.
    supply_route_integrity:
        Indicator on a ``[0, 1]`` scale for route continuity.
    market_access:
        Fractional indicator on a ``[0, 1]`` scale for customer access.
    currency_stability:
        Fractional indicator on a ``[0, 1]`` scale for payment stability.
    aid_dependency:
        Fractional indicator on a ``[0, 1]`` scale where higher means local
        commerce depends more on external aid. This reduces viability.
    """

    region: str
    security_score: float
    supply_route_integrity: float
    market_access: float
    currency_stability: float
    aid_dependency: float = 0.0

    def __post_init__(self) -> None:
        if not isinstance(self.region, str) or not self.region.strip():
            raise ValueError("region must be a non-empty string")

        metrics = {
            "security_score": self.security_score,
            "supply_route_integrity": self.supply_route_integrity,
            "market_access": self.market_access,
            "currency_stability": self.currency_stability,
            "aid_dependency": self.aid_dependency,
        }
        for name, value in metrics.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")


@dataclass(frozen=True)
class WarZoneCommerceAssessment:
    """Aggregated commerce viability for a region."""

    region: str
    viability_score: float
    commerce_state: str
    signal_count: int


def model_war_zone_commerce(
    signals: Sequence[CommerceSignal],
    *,
    security_weight: float = 0.35,
    logistics_weight: float = 0.25,
    access_weight: float = 0.2,
    currency_weight: float = 0.1,
    aid_penalty_weight: float = 0.1,
    min_viability: float = 0.0,
) -> tuple[WarZoneCommerceAssessment, ...]:
    """Estimate commerce viability by region from a series of signals."""

    if not 0.0 <= min_viability <= 1.0:
        raise ValueError("min_viability must be between 0 and 1")

    positive_total = security_weight + logistics_weight + access_weight + currency_weight
    if positive_total <= 0:
        raise ValueError("At least one positive weight must be > 0")
    if aid_penalty_weight < 0:
        raise ValueError("aid_penalty_weight must be non-negative")

    aggregates: Dict[str, Dict[str, float]] = {}
    for signal in signals:
        region = signal.region.strip()
        bucket = aggregates.setdefault(region, {"score": 0.0, "count": 0.0})

        positive_component = (
            security_weight * signal.security_score
            + logistics_weight * signal.supply_route_integrity
            + access_weight * signal.market_access
            + currency_weight * signal.currency_stability
        ) / positive_total
        penalty = aid_penalty_weight * signal.aid_dependency
        score = _clamp(positive_component - penalty)

        bucket["score"] += score
        bucket["count"] += 1.0

    assessments = []
    for region, data in aggregates.items():
        avg_score = data["score"] / data["count"]
        avg_score = _clamp(avg_score)
        if avg_score < min_viability:
            continue

        assessments.append(
            WarZoneCommerceAssessment(
                region=region,
                viability_score=avg_score,
                commerce_state=_state_from_score(avg_score),
                signal_count=int(data["count"]),
            )
        )

    assessments.sort(key=lambda item: item.viability_score, reverse=True)
    return tuple(assessments)


def _state_from_score(score: float) -> str:
    if score >= 0.75:
        return "operational"
    if score >= 0.45:
        return "fragile"
    return "collapsed"


def _clamp(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value
