"""Tests for the fungal species estimation utilities."""

import math
import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "modules" / "jb_bootcamp"
if str(MODULE_PATH) not in sys.path:
    sys.path.insert(0, str(MODULE_PATH))


from jb_bootcamp import EnvironmentParameters, estimate_fungal_species_numbers


def test_estimation_grows_with_positive_influx():
    """A healthy environment with influx should grow the population."""

    env = EnvironmentParameters(
        earth_size=1.2,
        water_level=0.8,
        forest_temperature=21.0,
        landscape_loading=0.1,
    )
    influx = [50.0] * 10
    efflux = [10.0] * 10

    history = estimate_fungal_species_numbers(
        influx,
        efflux,
        initial_population=1_000.0,
        environment=env,
    )

    assert history[0] == pytest.approx(1_000.0)
    assert history[-1] > history[0]
    assert all(val >= 0 for val in history)


def test_zero_time_step_not_allowed():
    """The estimator should reject non-positive time steps."""

    with pytest.raises(ValueError):
        estimate_fungal_species_numbers([], [], time_step=0)


def test_high_landscape_loading_limits_capacity():
    """Stressful environments should not allow divergence."""

    env = EnvironmentParameters(earth_size=1.0, water_level=0.9, landscape_loading=0.9)
    influx = [0.0] * 20
    efflux = [0.0] * 20

    history = estimate_fungal_species_numbers(
        influx,
        efflux,
        initial_population=5_000.0,
        environment=env,
        base_growth_rate=0.5,
    )

    assert math.isfinite(history[-1])
    assert history[-1] <= 10_000
