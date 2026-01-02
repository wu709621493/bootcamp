"""Simple helpers for emergency exit planning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

__all__ = ["Exit", "exit_throughput", "estimate_evacuation_time"]


@dataclass(frozen=True)
class Exit:
    """Representation of a single emergency exit."""

    width_m: float
    distance_m: float = 0.0
    congested: bool = False

    def __post_init__(self) -> None:  # pragma: no cover - straightforward validation
        if self.width_m <= 0:
            raise ValueError("width_m must be positive")
        if self.distance_m < 0:
            raise ValueError("distance_m must be non-negative")


def exit_throughput(
    exit_: Exit,
    *,
    flow_rate_per_meter: float = 1.3,
    congestion_penalty: float = 0.25,
) -> float:
    """Return expected people-per-second throughput for an exit.

    The ``flow_rate_per_meter`` parameter defaults to the common 1.3 people per
    second per metre guideline. When ``exit_.congested`` is ``True``, the
    congestion penalty reduces the throughput accordingly.
    """

    if flow_rate_per_meter <= 0:
        raise ValueError("flow_rate_per_meter must be positive")
    if not 0.0 <= congestion_penalty < 1.0:
        raise ValueError("congestion_penalty must be in [0, 1)")

    throughput = exit_.width_m * flow_rate_per_meter
    if exit_.congested:
        throughput *= 1.0 - congestion_penalty
    return throughput


def estimate_evacuation_time(
    occupants: int,
    exits: Iterable[Exit],
    *,
    average_travel_time: float = 30.0,
    flow_rate_per_meter: float = 1.3,
    congestion_penalty: float = 0.25,
) -> float:
    """Estimate total evacuation time in seconds.

    The calculation combines a fixed average travel time with the time required
    for occupants to pass through the available exits. The estimate is intended
    for quick comparisons rather than detailed engineering analysis.
    """

    if occupants <= 0:
        raise ValueError("occupants must be positive")
    if average_travel_time < 0:
        raise ValueError("average_travel_time must be non-negative")

    exits = tuple(exits)
    if not exits:
        raise ValueError("At least one exit must be provided")

    total_throughput = 0.0
    for exit_ in exits:
        total_throughput += exit_throughput(
            exit_,
            flow_rate_per_meter=flow_rate_per_meter,
            congestion_penalty=congestion_penalty,
        )

    if total_throughput <= 0:
        raise ValueError("Total throughput must be positive")

    return average_travel_time + occupants / total_throughput
