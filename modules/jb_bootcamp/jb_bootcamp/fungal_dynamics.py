"""Utilities for estimating fungal species numbers using discrete dynamics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class EnvironmentParameters:
    """Container for environmental inputs used in the species estimator.

    Attributes
    ----------
    earth_size : float
        Relative size of the ecosystem under consideration.  This term is used
        as a multiplier on the carrying capacity.  Values larger than one
        represent access to a larger habitable area, whereas values smaller
        than one correspond to fragmented terrain.
    water_level : float
        Normalised representation (0.0 - 1.0) of water availability.  This
        value is used to scale the effective growth rate; low water levels slow
        down fungal reproduction while higher values promote it.
    forest_temperature : float
        Ambient temperature in degrees Celsius.  A mild temperate environment
        (roughly 20 ºC) is assumed to maximise growth, and deviations from this
        temperature decrease the effective growth rate.
    landscape_loading : float
        A stress term that captures human impact, nutrient depletion, or any
        other load on the landscape.  This factor diminishes the carrying
        capacity as it increases.
    """

    earth_size: float = 1.0
    water_level: float = 0.7
    forest_temperature: float = 20.0
    landscape_loading: float = 0.2


def _scale_growth_rate(base_growth_rate: float, env: EnvironmentParameters) -> float:
    """Return a growth rate adjusted by environmental modifiers."""

    # Water availability linearly boosts or reduces the growth rate.
    water_adjustment = 0.5 + env.water_level

    # Penalise deviations from an optimal temperature of 20 ºC.
    optimal_temperature = 20.0
    temperature_penalty = 1.0 - min(abs(env.forest_temperature - optimal_temperature) / 40.0, 0.8)

    return base_growth_rate * water_adjustment * temperature_penalty


def _scale_carrying_capacity(
    base_capacity: float, env: EnvironmentParameters
) -> float:
    """Return a carrying capacity adjusted for area and landscape load."""

    capacity = base_capacity * max(env.earth_size, 0.0)
    # Landscape loading is treated as a pressure that reduces available niches.
    return capacity * max(1.0 - env.landscape_loading, 0.05)


def estimate_fungal_species_numbers(
    influx: Iterable[float],
    efflux: Iterable[float],
    *,
    initial_population: float = 1_000.0,
    base_growth_rate: float = 0.15,
    base_carrying_capacity: float = 100_000.0,
    time_step: float = 1.0,
    environment: EnvironmentParameters | None = None,
) -> List[float]:
    """Estimate fungal species numbers using a discrete logistic model.

    The estimator follows a simple difference equation that combines a
    logistic growth model with externally supplied influx and efflux terms.
    This captures dispersal (influx) and loss (efflux) of species within a
    habitat, all modulated by the state of the environment.

    Parameters
    ----------
    influx, efflux
        Iterable time series describing immigration (influx) and emigration or
        attrition (efflux) of species.  The iterables must be of identical
        length.
    initial_population
        Number of species present before the simulation begins.
    base_growth_rate
        Intrinsic per-step growth rate used before environmental adjustment.
    base_carrying_capacity
        Carrying capacity prior to environmental adjustments.
    time_step
        Size of the discrete time step used in the difference equation.
    environment
        Optional :class:`EnvironmentParameters` instance.  If ``None``,
        defaults that represent a moderately healthy forest are used.

    Returns
    -------
    list of float
        Estimated species counts for each time step, including the initial
        population as the first entry.

    Raises
    ------
    ValueError
        If the influx and efflux series do not contain the same number of
        observations or if any parameter would yield non-physical behaviour.
    """

    influx = list(influx)
    efflux = list(efflux)

    if len(influx) != len(efflux):
        raise ValueError("Influx and efflux series must have the same length.")

    if time_step <= 0:
        raise ValueError("Time step must be positive.")

    if initial_population < 0:
        raise ValueError("Initial population must be non-negative.")

    env = environment or EnvironmentParameters()
    growth_rate = _scale_growth_rate(base_growth_rate, env)
    carrying_capacity = _scale_carrying_capacity(base_carrying_capacity, env)

    if carrying_capacity <= 0:
        raise ValueError("Carrying capacity must be positive after scaling.")

    population = initial_population
    history = [population]

    for step_influx, step_efflux in zip(influx, efflux):
        logistic_term = growth_rate * population * (1.0 - population / carrying_capacity)
        population = max(
            population + time_step * logistic_term + step_influx - step_efflux,
            0.0,
        )
        history.append(population)

    return history


__all__ = [
    "EnvironmentParameters",
    "estimate_fungal_species_numbers",
]

