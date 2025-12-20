import math

import pytest

from jb_bootcamp.spin import angular_momentum, rotational_energy, spin_up


def test_angular_momentum_basic():
    assert angular_momentum(2.5, 4.0) == pytest.approx(10.0)


def test_rotational_energy_basic():
    assert rotational_energy(3.0, 2.0) == pytest.approx(6.0)


def test_spin_up_accelerates_with_torque():
    final_omega = spin_up(initial_omega=1.5, torque=5.0, moment_of_inertia=2.0, duration=3.0)
    assert final_omega == pytest.approx(1.5 + (5.0 / 2.0) * 3.0)


def test_spin_up_handles_zero_torque():
    assert spin_up(initial_omega=10.0, torque=0.0, moment_of_inertia=4.0, duration=5.0) == pytest.approx(10.0)


def test_negative_duration_errors():
    with pytest.raises(ValueError):
        spin_up(initial_omega=0.0, torque=1.0, moment_of_inertia=2.0, duration=-1.0)


def test_negative_inertia_errors():
    with pytest.raises(ValueError):
        angular_momentum(-1.0, 3.0)

    with pytest.raises(ValueError):
        rotational_energy(0.0, math.pi)
