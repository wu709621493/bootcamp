"""Tests for temperature conversion and summary helpers."""

import math
import pytest

from jb_bootcamp.temperature import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    mean_temperature,
    temperature_range,
)


def test_conversion_pairs():
    freezing_f = celsius_to_fahrenheit(0)
    boiling_f = celsius_to_fahrenheit(100)

    assert math.isclose(freezing_f, 32)
    assert math.isclose(boiling_f, 212)
    assert math.isclose(fahrenheit_to_celsius(freezing_f), 0)
    assert math.isclose(fahrenheit_to_celsius(boiling_f), 100)


def test_mean_and_range_values():
    readings = [18.5, 21.0, 19.5, 23.0]
    assert math.isclose(mean_temperature(readings), 20.5)
    assert math.isclose(temperature_range(readings), 4.5)


def test_validation_errors():
    with pytest.raises(TypeError):
        celsius_to_fahrenheit(True)
    with pytest.raises(TypeError):
        fahrenheit_to_celsius("hot")

    with pytest.raises(ValueError):
        mean_temperature([])

    with pytest.raises(TypeError):
        temperature_range([10, None])
