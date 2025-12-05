"""Utilities for evaluating urban skyline envelopes.

Project Skyline provides helpers for quickly sketching the silhouette of a
city block and checking whether proposed buildings respect a view corridor
that slopes upward from a protected vantage point.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

__all__ = [
    "BuildingPlan",
    "ViewCorridor",
    "skyline_outline",
    "corridor_clearance",
]


@dataclass(frozen=True)
class BuildingPlan:
    """Representation of a rectangular building footprint."""

    start: float
    end: float
    height: float
    name: str | None = None

    def __post_init__(self) -> None:  # pragma: no cover - defensive checks
        if self.start >= self.end:
            raise ValueError("start must be smaller than end")
        if self.height <= 0:
            raise ValueError("height must be positive")


@dataclass(frozen=True)
class ViewCorridor:
    """View-plane that sets the maximum allowed height at each position."""

    origin: float
    base_height: float
    slope_per_meter: float = 0.0

    def allowed_height(self, position: float) -> float:
        offset = abs(position - self.origin)
        return self.base_height + self.slope_per_meter * offset


KeyPoint = Tuple[float, float]


def skyline_outline(plans: Sequence[BuildingPlan]) -> list[KeyPoint]:
    """Compute the skyline outline for the provided building plans."""

    events: list[tuple[float, float, float]] = []
    for plan in plans:
        events.append((plan.start, -plan.height, plan.end))
        events.append((plan.end, 0.0, plan.end))

    if not events:
        return []

    events.sort()
    outline: list[KeyPoint] = []
    live: list[tuple[float, float]] = [(0.0, float("inf"))]
    previous_height = 0.0
    idx = 0
    n_events = len(events)

    while idx < n_events:
        current_x = events[idx][0]
        while idx < n_events and events[idx][0] == current_x:
            x, height, end = events[idx]
            if height < 0:
                live.append((height, end))
            else:
                # Record the end boundary so it can be dropped once passed.
                live.append((height, end))
            idx += 1

        live = [entry for entry in live if entry[1] > current_x]
        live.sort()
        current_height = -live[0][0] if live else 0.0

        if current_height != previous_height:
            outline.append((current_x, current_height))
            previous_height = current_height

    if outline and outline[-1][1] != 0.0:
        last_x = max(end for _, _, end in events)
        outline.append((last_x, 0.0))

    return outline


def corridor_clearance(
    plans: Iterable[BuildingPlan], corridor: ViewCorridor
) -> tuple[float, list[str]]:
    """Return the compliance ratio and list of violating plan names."""

    total_span = 0.0
    violating_span = 0.0
    violators: list[str] = []

    for idx, plan in enumerate(plans):
        span = plan.end - plan.start
        total_span += span

        allowed = corridor.allowed_height(plan.start)
        alt_allowed = corridor.allowed_height(plan.end)
        permitted_height = min(allowed, alt_allowed)

        if plan.height > permitted_height:
            violating_span += span
            violators.append(plan.name or f"plan_{idx}")

    if total_span == 0:
        raise ValueError("At least one plan with non-zero span is required")

    compliance = max(0.0, 1.0 - violating_span / total_span)
    return round(compliance, 3), violators
