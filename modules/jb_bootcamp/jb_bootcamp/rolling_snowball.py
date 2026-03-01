"""Prototype solvers for an NP-hard rolling-snowball planning problem.

A snowball starts at a launch point with an initial mass. Visiting a patch of snow
adds mass, while travel time melts mass at a fixed rate. The optimization asks for
an order (and subset) of patches that maximizes final mass under a time budget.

This contains the NP-hard core of orienteering / prize-collecting tour planning,
so this module provides:

* an exact exponential-time search for small instances;
* a greedy heuristic for quick approximations.
"""

from __future__ import annotations

from itertools import permutations
from typing import Mapping

__all__ = [
    "optimal_snowball_route",
    "greedy_snowball_route",
]


def optimal_snowball_route(
    start: str,
    patch_gain: Mapping[str, float],
    travel_minutes: Mapping[tuple[str, str], float],
    time_budget: float,
    *,
    initial_mass: float = 1.0,
    melt_rate_per_minute: float = 0.05,
) -> tuple[tuple[str, ...], float, float]:
    """Return the exact best route, final mass, and time used.

    The route may skip patches if visiting them is not beneficial or feasible.
    """

    _validate_inputs(
        start,
        patch_gain,
        travel_minutes,
        time_budget,
        initial_mass,
        melt_rate_per_minute,
    )

    patches = tuple(patch_gain)
    best_route: tuple[str, ...] = ()
    best_mass = initial_mass
    best_time = 0.0

    for r in range(1, len(patches) + 1):
        for order in permutations(patches, r):
            time_used = _route_time(start, order, travel_minutes)
            if time_used > time_budget:
                continue
            mass = initial_mass + _route_gain(order, patch_gain) - melt_rate_per_minute * time_used
            if mass > best_mass:
                best_route = order
                best_mass = mass
                best_time = time_used

    return best_route, best_mass, best_time


def greedy_snowball_route(
    start: str,
    patch_gain: Mapping[str, float],
    travel_minutes: Mapping[tuple[str, str], float],
    time_budget: float,
    *,
    initial_mass: float = 1.0,
    melt_rate_per_minute: float = 0.05,
) -> tuple[tuple[str, ...], float, float]:
    """Return a greedy route that picks the best immediate net mass increase."""

    _validate_inputs(
        start,
        patch_gain,
        travel_minutes,
        time_budget,
        initial_mass,
        melt_rate_per_minute,
    )

    remaining = set(patch_gain)
    current = start
    route: list[str] = []
    time_used = 0.0
    mass = initial_mass

    while remaining:
        best_patch = None
        best_delta = float("-inf")
        best_travel = 0.0

        for patch in remaining:
            travel = _edge_cost(current, patch, travel_minutes)
            if time_used + travel > time_budget:
                continue
            delta = patch_gain[patch] - melt_rate_per_minute * travel
            if delta > best_delta:
                best_delta = delta
                best_patch = patch
                best_travel = travel

        if best_patch is None or best_delta <= 0:
            break

        time_used += best_travel
        mass += best_delta
        route.append(best_patch)
        remaining.remove(best_patch)
        current = best_patch

    return tuple(route), mass, time_used


def _validate_inputs(
    start: str,
    patch_gain: Mapping[str, float],
    travel_minutes: Mapping[tuple[str, str], float],
    time_budget: float,
    initial_mass: float,
    melt_rate_per_minute: float,
) -> None:
    if not start:
        raise ValueError("start must be non-empty.")
    if time_budget <= 0:
        raise ValueError("time_budget must be positive.")
    if initial_mass <= 0:
        raise ValueError("initial_mass must be positive.")
    if melt_rate_per_minute < 0:
        raise ValueError("melt_rate_per_minute cannot be negative.")

    for patch, gain in patch_gain.items():
        if not patch:
            raise ValueError("patch names must be non-empty.")
        if patch == start:
            raise ValueError("patch names cannot include the start node.")
        if gain < 0:
            raise ValueError("patch gains must be non-negative.")

    for (a, b), minutes in travel_minutes.items():
        if not a or not b:
            raise ValueError("travel edge endpoints must be non-empty.")
        if minutes < 0:
            raise ValueError("travel times must be non-negative.")

    for patch in patch_gain:
        _edge_cost(start, patch, travel_minutes)
    patch_names = tuple(patch_gain)
    for i, a in enumerate(patch_names):
        for b in patch_names[i + 1 :]:
            _edge_cost(a, b, travel_minutes)


def _edge_cost(a: str, b: str, travel_minutes: Mapping[tuple[str, str], float]) -> float:
    if (a, b) in travel_minutes:
        return float(travel_minutes[(a, b)])
    if (b, a) in travel_minutes:
        return float(travel_minutes[(b, a)])
    raise KeyError(f"Missing travel-time edge between {a} and {b}.")


def _route_time(
    start: str,
    route: tuple[str, ...],
    travel_minutes: Mapping[tuple[str, str], float],
) -> float:
    total = 0.0
    current = start
    for patch in route:
        total += _edge_cost(current, patch, travel_minutes)
        current = patch
    return total


def _route_gain(route: tuple[str, ...], patch_gain: Mapping[str, float]) -> float:
    return float(sum(patch_gain[patch] for patch in route))
