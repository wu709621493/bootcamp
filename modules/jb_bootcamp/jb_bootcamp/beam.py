"""Lightweight helpers for sanity-checking rectangular beams."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BeamCheckResult:
    """Summary of a quick beam check under a uniformly distributed load.

    Parameters
    ----------
    bending_moment
        Maximum bending moment in Newton metres for the assumed loading.
    bending_stress
        Extreme-fibre bending stress in Pascals.
    deflection
        Midspan deflection in metres.
    stress_ok
        ``True`` if ``bending_stress`` does not exceed ``allowable_stress``.
    deflection_ok
        ``True`` if ``deflection`` is within the allowed limit ``span / ``
        ``deflection_limit_ratio``.
    """

    bending_moment: float
    bending_stress: float
    deflection: float
    stress_ok: bool
    deflection_ok: bool


def _require_positive(value: float, name: str) -> float:
    """Validate that a numerical parameter is positive.

    The helper reduces repetitive guard clauses while ensuring helpful error
    messages. It returns the provided ``value`` so the function can be used in
    expressions.
    """

    if value <= 0:
        raise ValueError(f"{name} must be positive; received {value!r}.")
    return value


def rectangular_moment_of_inertia(width: float, height: float) -> float:
    """Second moment of area for a rectangular cross-section.

    The inertia is computed about the neutral axis parallel to the width using
    the standard expression ``I = width * height**3 / 12``. Inputs must be
    positive; otherwise a :class:`ValueError` is raised.
    """

    width = _require_positive(width, "width")
    height = _require_positive(height, "height")
    return width * height ** 3 / 12.0


def rectangular_section_modulus(width: float, height: float) -> float:
    """Section modulus ``S`` for a rectangular cross-section.

    The modulus rescales the second moment of area to the outer fibre using the
    relation ``S = I / (height / 2)``. Inputs must be positive.
    """

    return rectangular_moment_of_inertia(width, height) / (height / 2.0)


def max_bending_moment_uniform_load(distributed_load: float, span: float) -> float:
    """Maximum bending moment for a simply supported beam with uniform load.

    The closed-form solution ``M_max = w * L**2 / 8`` is used, where ``w`` is
    the load intensity in Newtons per metre and ``L`` is the span length in
    metres. Both quantities must be positive.
    """

    distributed_load = _require_positive(distributed_load, "distributed_load")
    span = _require_positive(span, "span")
    return distributed_load * span ** 2 / 8.0


def midspan_deflection_uniform_load(
    distributed_load: float,
    span: float,
    youngs_modulus: float,
    moment_of_inertia: float,
) -> float:
    """Midspan deflection for a simply supported beam with uniform load.

    The analytical expression ``(5 * w * L**4) / (384 * E * I)`` is applied,
    where ``w`` is load intensity, ``L`` is span, ``E`` is Young's modulus, and
    ``I`` is the second moment of area. All parameters must be positive.
    """

    distributed_load = _require_positive(distributed_load, "distributed_load")
    span = _require_positive(span, "span")
    youngs_modulus = _require_positive(youngs_modulus, "youngs_modulus")
    moment_of_inertia = _require_positive(moment_of_inertia, "moment_of_inertia")
    return 5 * distributed_load * span ** 4 / (384.0 * youngs_modulus * moment_of_inertia)


def bending_stress(bending_moment: float, section_modulus: float) -> float:
    """Compute bending stress from a bending moment and section modulus.

    Stress is reported in Pascals and requires both inputs to be positive.
    """

    bending_moment = _require_positive(bending_moment, "bending_moment")
    section_modulus = _require_positive(section_modulus, "section_modulus")
    return bending_moment / section_modulus


def check_uniform_beam(
    *,
    span: float,
    distributed_load: float,
    width: float,
    height: float,
    youngs_modulus: float,
    allowable_stress: float,
    deflection_limit_ratio: float = 240.0,
) -> BeamCheckResult:
    """Perform a quick stress and deflection check for a uniform rectangular beam.

    The helper models a simply supported beam with a uniformly distributed load
    and reports whether the resulting bending stress and midspan deflection fall
    within common design limits.

    Parameters
    ----------
    span
        Beam span in metres.
    distributed_load
        Uniform load intensity in Newtons per metre.
    width, height
        Cross-sectional dimensions in metres.
    youngs_modulus
        Young's modulus in Pascals.
    allowable_stress
        Maximum allowable bending stress in Pascals.
    deflection_limit_ratio
        Ratio ``L / delta`` used for a deflection check. The default of 240 is a
        common serviceability criterion. Must be positive.
    """

    deflection_limit_ratio = _require_positive(deflection_limit_ratio, "deflection_limit_ratio")

    inertia = rectangular_moment_of_inertia(width, height)
    section_modulus = rectangular_section_modulus(width, height)
    moment = max_bending_moment_uniform_load(distributed_load, span)
    stress = bending_stress(moment, section_modulus)
    deflection = midspan_deflection_uniform_load(distributed_load, span, youngs_modulus, inertia)

    allowable_deflection = span / deflection_limit_ratio
    return BeamCheckResult(
        bending_moment=moment,
        bending_stress=stress,
        deflection=deflection,
        stress_ok=stress <= allowable_stress,
        deflection_ok=deflection <= allowable_deflection,
    )

