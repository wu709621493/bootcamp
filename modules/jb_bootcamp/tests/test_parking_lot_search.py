from __future__ import annotations

import pytest

from jb_bootcamp.parking_lot_search import (
    nearest_neighbor_search_order,
    optimal_search_order,
)


def test_optimal_search_order_finds_best_route() -> None:
    travel_minutes = {
        ("entrance", "A"): 5,
        ("entrance", "B"): 2,
        ("entrance", "C"): 4,
        ("A", "B"): 6,
        ("A", "C"): 1,
        ("B", "C"): 3,
    }

    order, total = optimal_search_order("entrance", ("A", "B", "C"), travel_minutes)

    assert order == ("B", "C", "A")
    assert total == pytest.approx(6)


def test_nearest_neighbor_uses_undirected_edges() -> None:
    travel_minutes = {
        ("A", "entrance"): 2,
        ("B", "entrance"): 7,
        ("B", "A"): 1,
    }

    order, total = nearest_neighbor_search_order("entrance", ("A", "B"), travel_minutes)

    assert order == ("A", "B")
    assert total == pytest.approx(3)


def test_rejects_invalid_or_incomplete_inputs() -> None:
    with pytest.raises(ValueError):
        optimal_search_order("", ("A",), {("entrance", "A"): 1})

    with pytest.raises(ValueError):
        nearest_neighbor_search_order("entrance", (), {})

    with pytest.raises(KeyError):
        optimal_search_order("entrance", ("A", "B"), {("entrance", "A"): 1, ("A", "B"): 1})

    with pytest.raises(ValueError):
        optimal_search_order(
            "entrance",
            ("A",),
            {
                ("entrance", "A"): -1,
            },
        )
