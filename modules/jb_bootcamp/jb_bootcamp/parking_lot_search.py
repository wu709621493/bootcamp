"""Route-planning helpers for searching a lost car in a large parking lot.

The core optimization asks for an order of candidate zones that minimizes total
walking time from the entrance while visiting every candidate exactly once.
This is equivalent to a shortest Hamiltonian path variant and is NP-hard,
so this module provides both an exact (factorial-time) solver and a cheap
nearest-neighbor heuristic.
"""

from __future__ import annotations

from itertools import permutations
from math import inf
from typing import Iterable, Mapping, Sequence

__all__ = [
    "optimal_search_order",
    "nearest_neighbor_search_order",
]


def optimal_search_order(
    start: str,
    candidate_zones: Sequence[str],
    travel_minutes: Mapping[tuple[str, str], float],
) -> tuple[tuple[str, ...], float]:
    """Return the exact minimum-time search order and its travel time.

    Parameters
    ----------
    start:
        Entrance or current position.
    candidate_zones:
        Zones where the car might be parked.
    travel_minutes:
        Non-negative pairwise travel-time map, keyed by ``(zone_a, zone_b)``.
        The map may include one direction only; lookups are treated as
        undirected by checking the reversed pair.
    """

    zones = tuple(candidate_zones)
    _validate_inputs(start, zones, travel_minutes)

    best_order: tuple[str, ...] | None = None
    best_cost = inf
    for order in permutations(zones):
        cost = _route_cost(start, order, travel_minutes)
        if cost < best_cost:
            best_cost = cost
            best_order = order

    assert best_order is not None  # zones cannot be empty after validation
    return best_order, best_cost


def nearest_neighbor_search_order(
    start: str,
    candidate_zones: Sequence[str],
    travel_minutes: Mapping[tuple[str, str], float],
) -> tuple[tuple[str, ...], float]:
    """Return a greedy order that picks the closest unvisited zone each step."""

    zones = tuple(candidate_zones)
    _validate_inputs(start, zones, travel_minutes)

    remaining = set(zones)
    current = start
    order: list[str] = []
    total = 0.0

    while remaining:
        next_zone = min(remaining, key=lambda zone: _edge_cost(current, zone, travel_minutes))
        total += _edge_cost(current, next_zone, travel_minutes)
        order.append(next_zone)
        remaining.remove(next_zone)
        current = next_zone

    return tuple(order), total


def _validate_inputs(
    start: str,
    candidate_zones: Sequence[str],
    travel_minutes: Mapping[tuple[str, str], float],
) -> None:
    if not start:
        raise ValueError("start must be a non-empty zone name.")
    if not candidate_zones:
        raise ValueError("candidate_zones cannot be empty.")
    if len(set(candidate_zones)) != len(candidate_zones):
        raise ValueError("candidate_zones must be unique.")
    if start in candidate_zones:
        raise ValueError("start cannot also appear in candidate_zones.")

    required_pairs = list(_required_edges(start, candidate_zones))
    for a, b in required_pairs:
        cost = _edge_cost(a, b, travel_minutes)
        if cost < 0:
            raise ValueError("travel times must be non-negative.")


def _required_edges(start: str, zones: Sequence[str]) -> Iterable[tuple[str, str]]:
    nodes = (start, *zones)
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            yield a, b


def _edge_cost(a: str, b: str, travel_minutes: Mapping[tuple[str, str], float]) -> float:
    if (a, b) in travel_minutes:
        return float(travel_minutes[(a, b)])
    if (b, a) in travel_minutes:
        return float(travel_minutes[(b, a)])
    raise KeyError(f"Missing travel-time edge between {a} and {b}.")


def _route_cost(
    start: str,
    order: Sequence[str],
    travel_minutes: Mapping[tuple[str, str], float],
) -> float:
    total = 0.0
    current = start
    for zone in order:
        total += _edge_cost(current, zone, travel_minutes)
        current = zone
    return total
