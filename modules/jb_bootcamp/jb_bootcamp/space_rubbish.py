"""Space rubbish scavenger hunting game mechanics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, MutableMapping, Tuple

__all__ = ["Rubbish", "SpaceRubbishGame"]


@dataclass(frozen=True)
class Rubbish:
    """A piece of space rubbish waiting to be scavenged."""

    name: str
    value: int


class SpaceRubbishGame:
    """Manage the state of a space rubbish scavenger hunt."""

    _STEP_VECTORS = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0),
    }

    def __init__(
        self,
        width: int,
        height: int,
        *,
        layout: Mapping[Tuple[int, int], Iterable[Tuple[str, int]] | Iterable[Rubbish]] | None = None,
        fuel: int = 20,
        start: Tuple[int, int] = (0, 0),
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        if fuel <= 0:
            raise ValueError("fuel must be positive")
        if not (0 <= start[0] < width and 0 <= start[1] < height):
            raise ValueError("start position must be within the field bounds")

        self.width = width
        self.height = height
        self.fuel = fuel
        self.position = start
        self.score = 0
        self._grid: MutableMapping[Tuple[int, int], List[Rubbish]] = {}

        if layout:
            for coordinates, items in layout.items():
                if not (0 <= coordinates[0] < width and 0 <= coordinates[1] < height):
                    raise ValueError("rubbish coordinates must be within the field bounds")
                rubbish_items = [self._coerce_item(item) for item in items]
                if rubbish_items:
                    self._grid[coordinates] = rubbish_items

    @staticmethod
    def _coerce_item(item: Rubbish | Tuple[str, int]) -> Rubbish:
        if isinstance(item, Rubbish):
            return item
        try:
            name, value = item
        except (TypeError, ValueError) as exc:  # pragma: no cover - defensive programming
            raise TypeError("items must be 2-tuples of (name, value)") from exc
        return Rubbish(str(name), int(value))

    @property
    def fuel_remaining(self) -> int:
        """Number of thrust units left for the scavenger ship."""

        return self.fuel

    def move(self, direction: str) -> Tuple[int, int]:
        """Move the scavenger ship in the given direction."""

        if direction not in self._STEP_VECTORS:
            raise ValueError(f"Unknown direction '{direction}'")
        if self.fuel <= 0:
            raise RuntimeError("No fuel remaining; the mission is over")

        dx, dy = self._STEP_VECTORS[direction]
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            raise ValueError("Cannot leave the bounds of the debris field")

        self.position = (new_x, new_y)
        self.fuel -= 1
        return self.position

    def collect(self) -> List[Rubbish]:
        """Collect all rubbish at the current position."""

        items = self._grid.pop(self.position, [])
        if items:
            self.score += sum(item.value for item in items)
        return items.copy()

    def scan(self, radius: int = 1) -> Dict[Tuple[int, int], Dict[str, int]]:
        """Scan surrounding sectors and summarize the findings."""

        if radius < 0:
            raise ValueError("radius must be non-negative")

        summary: Dict[Tuple[int, int], Dict[str, int]] = {}
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if max(abs(dx), abs(dy)) > radius:
                    continue
                x = self.position[0] + dx
                y = self.position[1] + dy
                if not (0 <= x < self.width and 0 <= y < self.height):
                    continue
                items = self._grid.get((x, y))
                if not items:
                    continue
                summary[(x, y)] = {
                    "count": len(items),
                    "value": sum(item.value for item in items),
                }
        return summary

    def remaining_items(self) -> int:
        """Return the number of remaining rubbish pieces in the field."""

        return sum(len(items) for items in self._grid.values())

    def is_over(self) -> bool:
        """Return whether the game has concluded."""

        return self.fuel <= 0 or self.remaining_items() == 0

    def status(self) -> Dict[str, int | Tuple[int, int]]:
        """Return a serializable summary of the current game state."""

        return {
            "position": self.position,
            "fuel": self.fuel,
            "score": self.score,
            "remaining_items": self.remaining_items(),
        }
