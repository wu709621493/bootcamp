"""Helpers for estimating whimsical borehole drilling missions."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi
from typing import Dict

__all__ = [
    "SOIL_RESISTANCE_FACTORS",
    "DrillingResult",
    "estimate_spoil_volume",
    "drill_hole",
]

SOIL_RESISTANCE_FACTORS: Dict[str, float] = {
    "sand": 0.75,
    "clay": 1.0,
    "loam": 0.9,
    "gravel": 1.3,
    "bedrock": 2.0,
}


@dataclass(frozen=True)
class DrillingResult:
    """Summary of a notional drilling attempt."""

    depth_m: float
    diameter_m: float
    soil_type: str
    spoil_volume_m3: float
    penetration_rate_m_per_hr: float
    duration_hr: float


def _validate_positive(value: float, *, name: str) -> float:
    """Validate that ``value`` is a positive real number and return it as float."""

    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric.")

    value = float(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive.")

    return value


def estimate_spoil_volume(depth_m: float, diameter_m: float) -> float:
    """Return the cylindrical spoil volume in cubic meters."""

    depth = _validate_positive(depth_m, name="depth_m")
    diameter = _validate_positive(diameter_m, name="diameter_m")
    radius = diameter / 2.0
    return pi * radius**2 * depth


def drill_hole(
    *,
    depth_m: float,
    diameter_m: float,
    soil_type: str,
    base_penetration_rate_m_per_hr: float = 0.6,
    downtime_fraction: float = 0.1,
) -> DrillingResult:
    """Estimate drilling effort for a playful borehole mission."""

    depth = _validate_positive(depth_m, name="depth_m")
    diameter = _validate_positive(diameter_m, name="diameter_m")

    if not isinstance(soil_type, str) or not soil_type.strip():
        raise ValueError("soil_type must be a non-empty string.")

    soil_key = soil_type.strip().lower()
    if soil_key not in SOIL_RESISTANCE_FACTORS:
        raise KeyError(
            f"Unknown soil_type '{soil_type}'. Known types: {', '.join(sorted(SOIL_RESISTANCE_FACTORS))}."
        )

    base_rate = _validate_positive(
        base_penetration_rate_m_per_hr, name="base_penetration_rate_m_per_hr"
    )

    if not isinstance(downtime_fraction, (int, float)):
        raise TypeError("downtime_fraction must be numeric.")

    downtime_fraction = float(downtime_fraction)
    if not 0 <= downtime_fraction < 1:
        raise ValueError("downtime_fraction must be between 0 (inclusive) and 1 (exclusive).")

    soil_factor = SOIL_RESISTANCE_FACTORS[soil_key]
    mechanical_rate = base_rate / soil_factor
    effective_rate = mechanical_rate * (1.0 - downtime_fraction)

    if effective_rate <= 0:
        raise ValueError(
            "Effective penetration rate is zero; adjust base rate or downtime_fraction."
        )

    spoil_volume = estimate_spoil_volume(depth, diameter)
    duration = depth / effective_rate

    return DrillingResult(
        depth_m=depth,
        diameter_m=diameter,
        soil_type=soil_key,
        spoil_volume_m3=spoil_volume,
        penetration_rate_m_per_hr=effective_rate,
        duration_hr=duration,
    )
