import math

import pytest

from jb_bootcamp.beam import (
    BeamCheckResult,
    bending_stress,
    check_uniform_beam,
    max_bending_moment_uniform_load,
    midspan_deflection_uniform_load,
    rectangular_moment_of_inertia,
    rectangular_section_modulus,
)


def test_rectangular_properties_and_moment():
    inertia = rectangular_moment_of_inertia(0.15, 0.3)
    modulus = rectangular_section_modulus(0.15, 0.3)

    assert math.isclose(inertia, 0.15 * 0.3 ** 3 / 12)
    assert math.isclose(modulus, inertia / (0.3 / 2))

    moment = max_bending_moment_uniform_load(8_000, 5.0)
    assert math.isclose(moment, 8_000 * 25 / 8)


def test_stress_and_deflection():
    inertia = rectangular_moment_of_inertia(0.2, 0.4)
    modulus = rectangular_section_modulus(0.2, 0.4)
    moment = max_bending_moment_uniform_load(5_000, 4.0)

    stress = bending_stress(moment, modulus)
    assert math.isclose(stress, moment / modulus)

    deflection = midspan_deflection_uniform_load(5_000, 4.0, 200e9, inertia)
    expected = 5 * 5_000 * 4.0 ** 4 / (384 * 200e9 * inertia)
    assert math.isclose(deflection, expected)


def test_uniform_check_flags_and_dataclass():
    result = check_uniform_beam(
        span=3.0,
        distributed_load=2_000,
        width=0.1,
        height=0.25,
        youngs_modulus=180e9,
        allowable_stress=120e6,
        deflection_limit_ratio=360,
    )

    assert isinstance(result, BeamCheckResult)
    assert result.stress_ok
    assert result.deflection_ok


@pytest.mark.parametrize(
    "func, kwargs",
    [
        (rectangular_moment_of_inertia, {"width": -1, "height": 0.3}),
        (rectangular_section_modulus, {"width": 0.0, "height": 0.3}),
        (max_bending_moment_uniform_load, {"distributed_load": 0, "span": 4}),
        (midspan_deflection_uniform_load, {"distributed_load": 1, "span": -2, "youngs_modulus": 1, "moment_of_inertia": 1}),
        (bending_stress, {"bending_moment": 1, "section_modulus": 0}),
        (
            check_uniform_beam,
            {
                "span": 1,
                "distributed_load": 1,
                "width": 1,
                "height": 1,
                "youngs_modulus": 1,
                "allowable_stress": 1,
                "deflection_limit_ratio": 0,
            },
        ),
    ],
)
def test_rejects_non_positive_inputs(func, kwargs):
    with pytest.raises(ValueError):
        func(**kwargs)

