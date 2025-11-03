"""Tests for the fluid dynamics helper functions."""

import math
import pathlib
import sys

import pytest


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


from jb_bootcamp import SwirlTransition, reynolds_number, swirl_state, swirl_transition_report


def test_reynolds_number_matches_manual_calculation():
    density = 1.225  # kg / m^3 (air at sea level)
    velocity = 12.0  # m / s
    length_scale = 0.35  # m
    dynamic_viscosity = 1.81e-5  # Pa * s

    expected = density * velocity * length_scale / dynamic_viscosity
    assert math.isclose(reynolds_number(density, velocity, length_scale, dynamic_viscosity), expected)


@pytest.mark.parametrize(
    "density, velocity, length_scale, dynamic_viscosity",
    [(-1.0, 1.0, 1.0, 1.0), (1.0, -1.0, 1.0, 1.0), (1.0, 1.0, -1.0, 1.0)],
)
def test_negative_inputs_raise_value_error(density, velocity, length_scale, dynamic_viscosity):
    with pytest.raises(ValueError):
        reynolds_number(density, velocity, length_scale, dynamic_viscosity)


def test_zero_viscosity_raises_value_error():
    with pytest.raises(ValueError):
        reynolds_number(1.0, 1.0, 1.0, 0.0)


@pytest.mark.parametrize(
    "reynolds, perturbation, obstacles, movers, expected",
    [
        (50.0, 0.0, 0.0, 0.0, "steady swirl"),
        (180.0, 0.0, 0.0, 0.0, "perturbed swirl"),
        (500.0, 0.5, 0.5, 0.5, "turbulence"),
    ],
)
def test_swirl_state_varies_with_modifiers(reynolds, perturbation, obstacles, movers, expected):
    assert (
        swirl_state(
            reynolds,
            perturbation_intensity=perturbation,
            obstacle_fraction=obstacles,
            moving_object_density=movers,
        )
        == expected
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"perturbation_intensity": -0.1},
        {"obstacle_fraction": 1.2},
        {"moving_object_density": 2.0},
    ],
)
def test_swirl_state_rejects_out_of_bounds_modifiers(kwargs):
    with pytest.raises(ValueError):
        swirl_state(100.0, **kwargs)


def test_swirl_transition_report_sequences_states():
    report = swirl_transition_report(
        density=998.0,
        velocity=0.3,
        length_scale=0.1,
        dynamic_viscosity=1e-3,
        perturbation_intensity=0.3,
        obstacle_fraction=0.4,
        moving_object_density=0.2,
    )

    assert isinstance(report, SwirlTransition)
    assert report.sequence[0] == "steady swirl"
    assert report.sequence[-1] == report.state
    assert set(report.sequence).issubset({"steady swirl", "perturbed swirl", "turbulence"})
