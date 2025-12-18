"""Elementary rifle ballistics utilities.

The helpers in this module intentionally ignore aerodynamic drag so that the
trajectory can be described with closed-form equations suitable for classroom
exercises.  They provide quick estimates for muzzle energy and bullet drop
relative to a sight line zeroed at a chosen distance.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

__all__ = [
    "TrajectoryPoint",
    "muzzle_energy",
    "predict_drop",
    "trajectory_profile",
]


@dataclass(frozen=True)
class TrajectoryPoint:
    """Snapshot of a simplified bullet flight path."""

    distance_m: float
    drop_m: float
    time_s: float


def muzzle_energy(bullet_mass_grams: float, muzzle_velocity_m_per_s: float) -> float:
    """Compute muzzle energy in joules from bullet mass (grams) and speed.

    The calculation uses ``E = 0.5 * m * v^2`` with ``m`` in kilograms.
    """

    if bullet_mass_grams <= 0:
        raise ValueError("bullet_mass_grams must be positive.")
    if muzzle_velocity_m_per_s < 0:
        raise ValueError("muzzle_velocity_m_per_s cannot be negative.")

    mass_kg = bullet_mass_grams / 1000.0
    return 0.5 * mass_kg * muzzle_velocity_m_per_s**2


def _zeroing_angle(
    muzzle_velocity_m_per_s: float,
    zero_range_m: float,
    sight_height_m: float,
    gravity: float,
) -> float:
    """Solve for the bore angle that intersects the sight line at ``zero_range_m``."""

    if muzzle_velocity_m_per_s <= 0:
        raise ValueError("muzzle_velocity_m_per_s must be positive.")
    if zero_range_m <= 0:
        raise ValueError("zero_range_m must be positive.")
    if sight_height_m < 0:
        raise ValueError("sight_height_m cannot be negative.")
    if gravity <= 0:
        raise ValueError("gravity must be positive.")

    v = muzzle_velocity_m_per_s
    x = zero_range_m
    y = sight_height_m
    radicand = v**4 - gravity * (gravity * x**2 + 2 * y * v**2)
    if radicand <= 0:
        raise ValueError("The sight line cannot be zeroed at the requested range.")

    tan_theta = (v**2 - math.sqrt(radicand)) / (gravity * x)
    return math.atan(tan_theta)


def _trajectory_height(
    distance_m: float, muzzle_velocity_m_per_s: float, angle: float, gravity: float
) -> tuple[float, float]:
    """Return (height, time) at ``distance_m`` for a projectile launched at ``angle``."""

    if distance_m < 0:
        raise ValueError("distance_m cannot be negative.")
    horizontal_velocity = muzzle_velocity_m_per_s * math.cos(angle)
    time = distance_m / horizontal_velocity
    vertical_velocity = muzzle_velocity_m_per_s * math.sin(angle)
    height = vertical_velocity * time - 0.5 * gravity * time**2
    return height, time


def predict_drop(
    distance_m: float,
    muzzle_velocity_m_per_s: float,
    *,
    zero_range_m: float = 100.0,
    sight_height_m: float = 0.05,
    gravity: float = 9.81,
) -> float:
    """Estimate bullet drop relative to the sight line at ``distance_m``.

    A positive value means the bullet is below the sight line; negative means it is
    still climbing above the point of aim.
    """

    angle = _zeroing_angle(muzzle_velocity_m_per_s, zero_range_m, sight_height_m, gravity)
    height, _ = _trajectory_height(distance_m, muzzle_velocity_m_per_s, angle, gravity)
    return sight_height_m - height


def trajectory_profile(
    distances_m: Sequence[float] | Iterable[float],
    muzzle_velocity_m_per_s: float,
    *,
    zero_range_m: float = 100.0,
    sight_height_m: float = 0.05,
    gravity: float = 9.81,
) -> tuple[TrajectoryPoint, ...]:
    """Build a simplified trajectory table for the provided distances."""

    angle = _zeroing_angle(muzzle_velocity_m_per_s, zero_range_m, sight_height_m, gravity)
    profile: list[TrajectoryPoint] = []
    for distance in distances_m:
        height, time = _trajectory_height(distance, muzzle_velocity_m_per_s, angle, gravity)
        drop = sight_height_m - height
        profile.append(TrajectoryPoint(distance, drop, time))
    return tuple(profile)
