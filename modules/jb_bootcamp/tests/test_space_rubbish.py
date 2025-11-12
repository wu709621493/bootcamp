"""Tests for the space rubbish scavenger hunting game."""

from __future__ import annotations

import pathlib
import sys


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


from jb_bootcamp.space_rubbish import Rubbish, SpaceRubbishGame


def build_game(fuel: int = 8) -> SpaceRubbishGame:
    layout = {
        (0, 0): [("solar panel", 5)],
        (1, 0): [("antenna", 7), ("paint chip", 3)],
        (2, 1): [("sat-core", 10)],
    }
    return SpaceRubbishGame(width=3, height=3, layout=layout, fuel=fuel)


def test_collecting_rubbish_increases_score():
    game = build_game()

    collected = game.collect()
    assert [item.name for item in collected] == ["solar panel"]
    assert game.score == 5
    assert game.remaining_items() == 3

    game.move("right")
    collected = game.collect()
    assert sorted(item.name for item in collected) == ["antenna", "paint chip"]
    assert game.score == 15
    assert game.remaining_items() == 1
    assert not game.is_over()

    game.move("down")
    assert game.collect() == []
    game.move("right")
    assert [item.name for item in game.collect()] == ["sat-core"]
    assert game.score == 25
    assert game.is_over()


def test_scan_reports_items_in_radius():
    game = build_game()
    report = game.scan(radius=2)

    assert report == {
        (0, 0): {"count": 1, "value": 5},
        (1, 0): {"count": 2, "value": 10},
        (2, 1): {"count": 1, "value": 10},
    }

    # Clear the starting sector before moving on.
    game.collect()
    game.move("right")
    game.collect()
    # The scan should no longer include the cleared sector.
    report = game.scan(radius=1)
    assert report == {
        (2, 1): {"count": 1, "value": 10},
    }


def test_movement_rules_and_fuel_usage():
    game = build_game(fuel=3)

    assert game.fuel_remaining == 3
    game.move("right")
    assert game.position == (1, 0)
    assert game.fuel_remaining == 2

    game.move("left")
    assert game.position == (0, 0)
    assert game.fuel_remaining == 1

    try:
        game.move("left")
    except ValueError as exc:
        assert "bounds" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected ValueError when leaving the field")

    game.move("right")
    assert game.fuel_remaining == 0

    try:
        game.move("up")
    except RuntimeError as exc:
        assert "No fuel" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected RuntimeError when fuel is depleted")

    try:
        game.move("diagonal")
    except ValueError as exc:
        assert "Unknown direction" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected ValueError for invalid direction")


def test_custom_layout_accepts_rubbish_objects():
    layout = {
        (0, 0): [Rubbish(name="booster", value=12)],
    }
    game = SpaceRubbishGame(width=2, height=2, layout=layout, fuel=2)

    assert game.collect()[0] == Rubbish(name="booster", value=12)
    assert game.score == 12
    assert game.is_over()
