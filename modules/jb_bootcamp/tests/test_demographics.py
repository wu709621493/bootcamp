from datetime import date

import pytest

from jb_bootcamp.demographics import (
    CohortBoundary,
    generation_from_age,
    generation_from_birth_year,
    normalise_age,
)


def test_normalise_age_handles_strings_and_numbers():
    assert normalise_age(" 35 years") == 35
    assert normalise_age(42) == 42
    assert normalise_age(19.8) == 19


@pytest.mark.parametrize(
    "raw_age",
    [None, "", "unknown", -2, float("inf"), float("nan"), True],
)
def test_normalise_age_rejects_invalid_values(raw_age):
    with pytest.raises((ValueError, TypeError)):
        normalise_age(raw_age)


def test_generation_from_birth_year_default_boundaries():
    assert generation_from_birth_year(1985) == "millennial"
    assert generation_from_birth_year(2001) == "generation_z"
    assert generation_from_birth_year(1946) == "boomer"


@pytest.mark.parametrize(
    "age,reference_year,expected",
    [
        (25, 2024, "generation_z"),
        (43, 2024, "millennial"),
        (10, 2024, "generation_alpha"),
    ],
)
def test_generation_from_age_with_reference_year(age, reference_year, expected):
    assert generation_from_age(age, reference_year=reference_year) == expected


def test_generation_from_age_uses_current_year_when_not_provided(monkeypatch):
    class FrozenDate(date):
        @classmethod
        def today(cls):
            return cls(2030, 6, 1)

    monkeypatch.setattr("jb_bootcamp.demographics.date", FrozenDate)
    assert generation_from_age(50) == "generation_x"


def test_generation_from_birth_year_custom_boundaries():
    boundaries = (
        CohortBoundary("ancient", None, 1899),
        CohortBoundary("modern", 1900, None),
    )
    assert generation_from_birth_year(1888, boundaries=boundaries) == "ancient"
    assert generation_from_birth_year(1999, boundaries=boundaries) == "modern"


def test_generation_from_age_validates_reference_year():
    with pytest.raises(TypeError):
        generation_from_age(30, reference_year="2020")
