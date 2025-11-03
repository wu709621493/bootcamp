"""Fluid-flow helpers for reasoning about swirl transitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SwirlTransition:
    """Structured summary of a swirl transition.

    Parameters
    ----------
    reynolds_number
        The Reynolds number associated with the flow conditions.
    state
        Final flow regime classification (``"steady swirl"``, ``"perturbed swirl"``,
        or ``"turbulence"``).
    sequence
        Ordered list of states encountered while the flow develops.
    """

    reynolds_number: float
    state: str
    sequence: tuple[str, ...]


def reynolds_number(density: float, velocity: float, length_scale: float, dynamic_viscosity: float) -> float:
    """Compute the Reynolds number for a flow configuration.

    Parameters
    ----------
    density
        Fluid density in kilograms per cubic metre.
    velocity
        Characteristic velocity in metres per second.
    length_scale
        Characteristic length scale in metres (e.g. obstacle diameter).
    dynamic_viscosity
        Dynamic viscosity in Pascal seconds.

    Returns
    -------
    float
        The Reynolds number ``Re = (density * velocity * length_scale) / dynamic_viscosity``.

    Raises
    ------
    ValueError
        Raised if any supplied quantity is negative or if ``dynamic_viscosity`` is
        zero.
    """

    for name, value in {
        "density": density,
        "velocity": velocity,
        "length_scale": length_scale,
        "dynamic_viscosity": dynamic_viscosity,
    }.items():
        if value < 0:
            raise ValueError(f"{name} must be non-negative, got {value!r}.")

    if dynamic_viscosity == 0:
        raise ValueError("dynamic_viscosity must be non-zero to compute a Reynolds number.")

    return density * velocity * length_scale / dynamic_viscosity


def _validate_unit_interval(value: float, name: str) -> float:
    """Ensure modifiers fall within the closed unit interval."""

    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1 (inclusive); received {value!r}.")
    return value


def swirl_state(
    reynolds: float,
    perturbation_intensity: float = 0.0,
    obstacle_fraction: float = 0.0,
    moving_object_density: float = 0.0,
) -> str:
    """Classify the swirl regime for a container with obstacles and movers.

    Parameters
    ----------
    reynolds
        Reynolds number for the base flow.
    perturbation_intensity
        Normalised magnitude (0-1) describing how strongly the flow is perturbed
        (e.g. shaking, pulsating inlets).
    obstacle_fraction
        Fraction (0-1) of the container cross-section blocked by obstacles.
    moving_object_density
        Effective density (0-1) of dense moving objects (e.g. particles or flyers)
        carried by the flow.

    Returns
    -------
    str
        One of ``"steady swirl"``, ``"perturbed swirl"``, or ``"turbulence"``.

    Notes
    -----
    The thresholds originate from a qualitative model: obstacles and dense movers
    reduce the Reynolds-number window that supports a steady swirl. Increased
    perturbations shrink the perturbed regime in favour of turbulence. The
    modifiers are dimensionless weights that compress the thresholds while
    remaining simple to reason about for exploratory bootcamp exercises.
    """

    if reynolds < 0:
        raise ValueError("Reynolds number must be non-negative.")

    perturbation_intensity = _validate_unit_interval(perturbation_intensity, "perturbation_intensity")
    obstacle_fraction = _validate_unit_interval(obstacle_fraction, "obstacle_fraction")
    moving_object_density = _validate_unit_interval(moving_object_density, "moving_object_density")

    # Base thresholds chosen to reflect the canonical laminar-to-turbulent shift.
    base_steady_limit = 150.0
    base_turbulent_onset = 950.0

    # Obstacles and dense movers reduce the stability window for steady swirls,
    # whereas perturbations bias the flow towards turbulence.
    modifier = 1 - (0.45 * obstacle_fraction + 0.35 * moving_object_density + 0.25 * perturbation_intensity)
    modifier = max(0.25, modifier)

    steady_limit = base_steady_limit * modifier
    turbulent_onset = base_turbulent_onset * modifier * (1 - 0.15 * perturbation_intensity)

    if reynolds < steady_limit:
        return "steady swirl"
    if reynolds < turbulent_onset:
        return "perturbed swirl"
    return "turbulence"


def swirl_transition_report(
    density: float,
    velocity: float,
    length_scale: float,
    dynamic_viscosity: float,
    perturbation_intensity: float = 0.0,
    obstacle_fraction: float = 0.0,
    moving_object_density: float = 0.0,
) -> SwirlTransition:
    """Bundle a flow state classification with a qualitative transition sequence.

    The report follows the steady → perturbed → turbulent storyline described in
    the prompt. Obstacles and dense movers are explicitly factored into the
    thresholds, making the helper useful for quick reasoning exercises while
    remaining simple enough to inspect during the bootcamp.
    """

    re_value = reynolds_number(density, velocity, length_scale, dynamic_viscosity)
    state = swirl_state(
        re_value,
        perturbation_intensity=perturbation_intensity,
        obstacle_fraction=obstacle_fraction,
        moving_object_density=moving_object_density,
    )

    sequence: list[str] = ["steady swirl"]
    if state in {"perturbed swirl", "turbulence"}:
        sequence.append("perturbed swirl")
    if state == "turbulence":
        sequence.append("turbulence")

    return SwirlTransition(re_value, state, tuple(sequence))
