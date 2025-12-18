import math

import pytest

from jb_bootcamp.rifle import TrajectoryPoint, muzzle_energy, predict_drop, trajectory_profile


def test_muzzle_energy():
    assert muzzle_energy(9, 820) == pytest.approx(3025.8, rel=1e-6)


@pytest.mark.parametrize(
    "distance_m, expected_drop_m",
    [
        (50, 0.006763059876974682),
        (100, 0.0),  # zero range, should align with sight line
        (200, 0.09589552093885333),
        (300, 0.33768656283923454),
    ],
)
def test_predict_drop(distance_m, expected_drop_m):
    drop = predict_drop(
        distance_m,
        muzzle_velocity_m_per_s=820.0,
        zero_range_m=100.0,
        sight_height_m=0.05,
    )
    assert drop == pytest.approx(expected_drop_m, rel=1e-12, abs=1e-10)


def test_trajectory_profile_points():
    distances = [0.0, 50.0, 100.0, 200.0]
    profile = trajectory_profile(distances, muzzle_velocity_m_per_s=820.0, sight_height_m=0.05)
    assert isinstance(profile, tuple)
    assert all(isinstance(point, TrajectoryPoint) for point in profile)

    for earlier, later in zip(profile, profile[1:]):
        assert later.distance_m > earlier.distance_m
        assert later.time_s > earlier.time_s

    assert profile[0].drop_m == pytest.approx(0.05, rel=1e-12)
    assert profile[2].drop_m == pytest.approx(0.0, abs=1e-10)

    # Trajectory should follow a parabola; expect upward curvature between zero and 200 m.
    assert profile[1].drop_m < profile[3].drop_m


def test_zero_range_unreachable():
    with pytest.raises(ValueError):
        predict_drop(
            50,
            muzzle_velocity_m_per_s=50.0,
            zero_range_m=500.0,
            sight_height_m=1.0,
        )
