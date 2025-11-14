"""Tests for the rocket landing simulation."""

import math
import pathlib
import sys


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


from jb_bootcamp import RocketState, simulate_vertical_landing


def test_simulation_returns_well_structured_history():
    result = simulate_vertical_landing()

    assert result.landed is True
    assert math.isclose(result.states[0].time, 0.0)
    assert isinstance(result.states[-1], RocketState)
    assert result.max_altitude > 100.0
    assert result.states[-1].altitude == 0.0
    assert abs(result.touchdown_velocity) <= 0.5


def test_reduced_thrust_requires_longer_landing_controller():
    result = simulate_vertical_landing(
        max_thrust=42000.0,
        controller_activation_altitude=180.0,
        damping_gain=1.5,
    )

    assert result.landed is True
    assert result.max_altitude > 100.0
    assert result.states[-1].time > 120.0
