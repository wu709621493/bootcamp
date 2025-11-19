"""Helpers for visualising Go boards on the floor or a ceiling mount."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Literal, Sequence, Tuple

Orientation = Literal["floor", "ceiling"]
_COLOR_ALIASES = {
    "B": "B",
    "BLACK": "B",
    "W": "W",
    "WHITE": "W",
}


def _normalise_orientation(orientation: str | Orientation) -> Orientation:
    value = orientation.lower()
    if value not in {"floor", "ceiling"}:
        raise ValueError(f"Unsupported orientation {orientation!r}.")
    return value  # type: ignore[return-value]


def transform_coordinate(row: int, column: int, *, size: int, orientation: str | Orientation) -> Tuple[int, int]:
    """Return how a ``(row, column)`` pair appears from the chosen orientation."""

    if not 1 <= row <= size:
        raise ValueError(f"row must be between 1 and {size}, got {row}.")
    if not 1 <= column <= size:
        raise ValueError(f"column must be between 1 and {size}, got {column}.")

    normalised = _normalise_orientation(orientation)
    if normalised == "floor":
        return (row, column)
    mirrored_row = size - row + 1
    mirrored_col = size - column + 1
    return (mirrored_row, mirrored_col)


@dataclass
class GoBoard:
    """Minimal representation of a Go board with orientation helpers."""

    size: int = 19
    _grid: List[List[str]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not 2 <= self.size <= 25:
            raise ValueError("Go board size must be between 2 and 25 lines.")
        self._grid = [["." for _ in range(self.size)] for _ in range(self.size)]

    def place_stone(self, color: str, row: int, column: int) -> None:
        normalized_color = self._normalise_color(color)
        target_row = self._to_internal_row(row)
        target_col = self._to_internal_col(column)
        if self._grid[target_row][target_col] != ".":
            raise ValueError("The requested point already contains a stone.")
        self._grid[target_row][target_col] = normalized_color

    def remove_stone(self, row: int, column: int) -> None:
        target_row = self._to_internal_row(row)
        target_col = self._to_internal_col(column)
        self._grid[target_row][target_col] = "."

    def snapshot(self, orientation: str | Orientation = "floor") -> Tuple[Tuple[str, ...], ...]:
        normalised = _normalise_orientation(orientation)
        row_indices = self._row_indices(normalised)
        column_indices = self._column_indices(normalised)
        return tuple(
            tuple(self._grid[row][column] for column in column_indices)
            for row in row_indices
        )

    def render(self, orientation: str | Orientation = "floor") -> str:
        grid = self.snapshot(orientation)
        normalised = _normalise_orientation(orientation)
        column_labels = self._column_labels(normalised)
        lines = ["   " + " ".join(column_labels)]
        row_labels = self._row_labels(normalised)
        for label, row in zip(row_labels, grid):
            lines.append(f"{label:>2} " + " ".join(row))
        return "\n".join(lines)

    def _normalise_color(self, color: str) -> str:
        key = color.strip().upper()
        if key not in _COLOR_ALIASES:
            raise ValueError(f"Unsupported stone colour {color!r}.")
        return _COLOR_ALIASES[key]

    def _to_internal_row(self, row: int) -> int:
        if not 1 <= row <= self.size:
            raise ValueError(f"row must be between 1 and {self.size}, got {row}.")
        return self.size - row

    def _to_internal_col(self, column: int) -> int:
        if not 1 <= column <= self.size:
            raise ValueError(f"column must be between 1 and {self.size}, got {column}.")
        return column - 1

    def _row_indices(self, orientation: Orientation) -> Iterable[int]:
        if orientation == "floor":
            return range(self.size - 1, -1, -1)
        return range(self.size)

    def _column_indices(self, orientation: Orientation) -> Iterable[int]:
        if orientation == "floor":
            return range(self.size)
        return range(self.size - 1, -1, -1)

    def _row_labels(self, orientation: Orientation) -> Sequence[int]:
        if orientation == "floor":
            return list(range(1, self.size + 1))
        return list(range(self.size, 0, -1))

    def _column_labels(self, orientation: Orientation) -> Sequence[str]:
        labels = [str(index) for index in range(1, self.size + 1)]
        if orientation == "ceiling":
            labels.reverse()
        return labels
