from __future__ import annotations

import pathlib
import sys

import pytest

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from jb_bootcamp.go_board import GoBoard, transform_coordinate


def test_snapshot_and_render_floor_vs_ceiling() -> None:
    board = GoBoard(size=5)
    board.place_stone("black", 1, 1)
    board.place_stone("white", 5, 5)

    floor_view = board.snapshot("floor")
    assert floor_view[0][0] == "B"
    assert floor_view[-1][-1] == "W"

    ceiling_view = board.snapshot("ceiling")
    assert ceiling_view[0][0] == "W"
    assert ceiling_view[-1][-1] == "B"

    render = board.render("ceiling")
    assert "5 4 3 2 1" in render.splitlines()[0]
    assert "5" in render.splitlines()[1]


def test_transform_coordinate_mirrors_for_ceiling() -> None:
    assert transform_coordinate(1, 3, size=9, orientation="floor") == (1, 3)
    assert transform_coordinate(1, 3, size=9, orientation="ceiling") == (9, 7)


@pytest.mark.parametrize("row,column", [(0, 1), (20, 30)])
def test_transform_coordinate_validates_bounds(row: int, column: int) -> None:
    with pytest.raises(ValueError):
        transform_coordinate(row, column, size=19, orientation="floor")


def test_place_stone_rejects_occupied_points() -> None:
    board = GoBoard(size=3)
    board.place_stone("b", 1, 1)
    with pytest.raises(ValueError):
        board.place_stone("white", 1, 1)

    board.remove_stone(1, 1)
    board.place_stone("white", 1, 1)
    rendered = board.render()
    assert rendered.splitlines()[1].endswith("W . .")
