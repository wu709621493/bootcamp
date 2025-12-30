"""Lightweight n-dimensional vector helper for bootcamp exercises."""

from __future__ import annotations

import math
from numbers import Number
from typing import Iterable, Iterator, Tuple


class Vector:
    """Immutable vector supporting basic arithmetic operations."""

    def __init__(self, *components: Number | Iterable[Number]):
        if len(components) == 1 and isinstance(components[0], Iterable) and not isinstance(
            components[0], (str, bytes)
        ):
            values = tuple(components[0])
        else:
            values = tuple(components)

        if not values:
            raise ValueError("Vector requires at least one component.")

        for value in values:
            if not isinstance(value, Number):
                raise TypeError("Vector components must be numeric.")

        self._components: Tuple[float, ...] = tuple(float(v) for v in values)

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._components)

    def __iter__(self) -> Iterator[float]:  # pragma: no cover - trivial
        return iter(self._components)

    def __getitem__(self, index: int) -> float:  # pragma: no cover - trivial
        return self._components[index]

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"Vector({', '.join(str(v) for v in self._components)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return self._components == other._components

    def _check_dimensions(self, other: "Vector") -> None:
        if len(self) != len(other):
            raise ValueError("Vectors must have the same dimension.")

    def __add__(self, other: "Vector") -> "Vector":
        self._check_dimensions(other)
        return Vector(a + b for a, b in zip(self, other))

    def __sub__(self, other: "Vector") -> "Vector":
        self._check_dimensions(other)
        return Vector(a - b for a, b in zip(self, other))

    def __mul__(self, other: Number | "Vector") -> "Vector" | float:
        if isinstance(other, Number):
            return Vector(a * float(other) for a in self)
        if isinstance(other, Vector):
            self._check_dimensions(other)
            return sum(a * b for a, b in zip(self, other))
        return NotImplemented

    def __rmul__(self, other: Number) -> "Vector":
        if isinstance(other, Number):
            return self.__mul__(other)  # type: ignore[return-value]
        return NotImplemented

    @property
    def magnitude(self) -> float:
        """Return the Euclidean length of the vector."""

        return math.sqrt(sum(component**2 for component in self))

    def normalize(self) -> "Vector":
        """Return a unit vector in the same direction.

        Raises
        ------
        ValueError
            If the vector has zero magnitude.
        """

        mag = self.magnitude
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector.")
        return Vector(component / mag for component in self)

    def distance_to(self, other: "Vector") -> float:
        """Return the Euclidean distance to ``other``."""

        return (self - other).magnitude
