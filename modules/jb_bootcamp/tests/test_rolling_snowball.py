from __future__ import annotations

import pytest

from jb_bootcamp.rolling_snowball import greedy_snowball_route, optimal_snowball_route


def test_optimal_snowball_route_picks_best_subset_and_order() -> None:
    patch_gain = {
        "A": 2.5,
        "B": 2.0,
        "C": 0.6,
    }
    travel_minutes = {
        ("S", "A"): 1,
        ("S", "B"): 4,
        ("S", "C"): 1,
        ("A", "B"): 1,
        ("A", "C"): 5,
        ("B", "C"): 1,
    }

    route, final_mass, time_used = optimal_snowball_route(
        "S",
        patch_gain,
        travel_minutes,
        time_budget=3,
        initial_mass=1.0,
        melt_rate_per_minute=0.5,
    )

    assert route == ("A", "B", "C")
    assert time_used == pytest.approx(3)
    assert final_mass == pytest.approx(4.6)


def test_greedy_route_stops_when_next_move_is_not_profitable() -> None:
    patch_gain = {
        "A": 1.0,
        "B": 0.1,
    }
    travel_minutes = {
        ("S", "A"): 1,
        ("S", "B"): 1,
        ("A", "B"): 3,
    }

    route, final_mass, time_used = greedy_snowball_route(
        "S",
        patch_gain,
        travel_minutes,
        time_budget=10,
        initial_mass=1.0,
        melt_rate_per_minute=0.5,
    )

    assert route == ("A",)
    assert time_used == pytest.approx(1)
    assert final_mass == pytest.approx(1.5)


def test_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        optimal_snowball_route("", {"A": 1}, {("S", "A"): 1}, time_budget=1)

    with pytest.raises(ValueError):
        greedy_snowball_route("S", {"A": -1}, {("S", "A"): 1}, time_budget=1)

    with pytest.raises(KeyError):
        optimal_snowball_route("S", {"A": 1, "B": 1}, {("S", "A"): 1}, time_budget=3)
