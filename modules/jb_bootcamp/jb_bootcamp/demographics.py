"""Helpers for normalising ages and mapping birth cohorts to generations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import math
import re
from typing import Iterable

__all__ = [
    "CohortBoundary",
    "normalise_age",
    "generation_from_birth_year",
    "generation_from_age",
    "DEFAULT_GENERATION_BOUNDARIES",
]


@dataclass(frozen=True)
class CohortBoundary:
    """Definition of a generational cohort."""

    name: str
    start_year: int | None
    end_year: int | None

    def includes(self, year: int) -> bool:
        if self.start_year is not None and year < self.start_year:
            return False
        if self.end_year is not None and year > self.end_year:
            return False
        return True


DEFAULT_GENERATION_BOUNDARIES: tuple[CohortBoundary, ...] = (
    CohortBoundary("greatest", None, 1927),
    CohortBoundary("silent", 1928, 1945),
    CohortBoundary("boomer", 1946, 1964),
    CohortBoundary("generation_x", 1965, 1980),
    CohortBoundary("millennial", 1981, 1996),
    CohortBoundary("generation_z", 1997, 2012),
    CohortBoundary("generation_alpha", 2013, None),
)


_NUMBER_PATTERN = re.compile(r"[-+]?\d+(?:\.\d+)?")


def _coerce_number(raw: object) -> float:
    if isinstance(raw, bool):
        raise TypeError("Boolean values are not valid ages.")
    if isinstance(raw, (int, float)):
        value = float(raw)
    elif isinstance(raw, str):
        text = raw.strip()
        if not text:
            raise ValueError("Empty strings cannot be interpreted as ages.")
        match = _NUMBER_PATTERN.search(text)
        if not match:
            raise ValueError(f"Could not parse an age from {raw!r}.")
        value = float(match.group())
    else:
        raise TypeError(f"Unsupported age type: {type(raw)!r}.")

    if math.isnan(value) or math.isinf(value):
        raise ValueError("Age must be a finite number.")
    if value < 0:
        raise ValueError("Age cannot be negative.")
    return value


def normalise_age(raw_age: object) -> int:
    """Convert loosely formatted age input to an integer number of years."""

    value = _coerce_number(raw_age)
    return int(value)


def generation_from_birth_year(
    birth_year: int,
    *,
    boundaries: Iterable[CohortBoundary] = DEFAULT_GENERATION_BOUNDARIES,
) -> str:
    """Return the generation label for ``birth_year``."""

    if not isinstance(birth_year, int):
        raise TypeError("Birth year must be an integer.")

    for boundary in boundaries:
        if boundary.includes(birth_year):
            return boundary.name
    raise ValueError(f"Birth year {birth_year} does not match any generation boundary.")


def generation_from_age(
    age: object,
    *,
    reference_year: int | None = None,
    boundaries: Iterable[CohortBoundary] = DEFAULT_GENERATION_BOUNDARIES,
) -> str:
    """Infer generation from an age value."""

    normalised_age = normalise_age(age)
    if reference_year is None:
        reference_year = date.today().year
    elif not isinstance(reference_year, int):
        raise TypeError("reference_year must be an integer when provided.")

    birth_year = reference_year - normalised_age
    return generation_from_birth_year(birth_year, boundaries=boundaries)
