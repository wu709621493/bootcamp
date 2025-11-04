"""Tools for simulating alien cultures from first principles.

The module encodes a small, deterministic system for reasoning about how
cultural traits respond to environmental pressures, innovation, and
inter-trait coupling.  The goal is to provide a playground for thinking about
plausible alien societies without relying on anthropocentric assumptions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Dict, Iterable, List, Mapping, Optional, Sequence


def _logistic(value: float) -> float:
    """Return the logistic activation of *value* with numerical stability."""
    if value >= 0:
        exp_neg = math.exp(-value)
        return 1.0 / (1.0 + exp_neg)
    exp_pos = math.exp(value)
    return exp_pos / (1.0 + exp_pos)


def _clamp_unit_interval(value: float) -> float:
    """Clamp *value* to the inclusive unit interval."""
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


@dataclass(frozen=True)
class CulturalTrait:
    """Description of a cultural trait tracked during simulation.

    Parameters
    ----------
    name:
        Human readable identifier for the trait.
    domain:
        Knowledge area that the trait belongs to (e.g. ritual, economy).
    initial_prevalence:
        Initial prevalence of the trait in the population.  This is a number
        between zero and one describing the proportion of the population that
        practices or endorses the trait.
    description:
        Optional free form text describing the role of the trait.
    """

    name: str
    domain: str
    initial_prevalence: float
    description: str = ""

    def __post_init__(self) -> None:  # pragma: no cover - validation is tested
        if not self.name:
            raise ValueError("A cultural trait must have a non-empty name.")
        if not self.domain:
            raise ValueError("A cultural trait must declare a domain.")
        if not 0.0 <= self.initial_prevalence <= 1.0:
            raise ValueError("Trait prevalence must be inside the [0, 1] interval.")


@dataclass(frozen=True)
class EnvironmentalFactor:
    """External force shaping trait adoption.

    Parameters
    ----------
    name:
        Identifier for the factor.
    weight:
        Overall strength of the factor.  Positive values amplify the stored
        domain level effects, while negative values invert them.
    effects:
        Mapping from domain name to influence coefficient.  The influence is
        multiplied by ``weight`` to obtain the final bias added to a trait's
        activation.
    description:
        Optional free form text capturing the significance of the factor.
    """

    name: str
    weight: float
    effects: Mapping[str, float] = field(default_factory=dict)
    description: str = ""

    def influence_for(self, domain: str) -> float:
        """Return the bias this factor exerts on *domain*."""
        return self.weight * self.effects.get(domain, 0.0)


class AlienCulture:
    """Stateful simulator for alien cultures.

    The simulator keeps track of trait prevalence and updates it using a
    logistic response to a weighted sum of drivers.  Drivers include:

    * intrinsic (baseline) bias for individual traits;
    * environmental factors coupling to trait domains;
    * pairwise interactions with other traits;
    * innovation impulses supplied by the caller.

    Parameters
    ----------
    traits:
        Iterable of :class:`CulturalTrait` defining the initial population
        state.
    baseline_bias:
        Optional mapping describing intrinsic biases per trait name.  Values
        shift the logistic response towards higher or lower prevalence.
    learning_rate:
        Fractional amount of the response that is applied each step.  Values
        in ``(0, 1]`` adapt quickly, while small values produce gradual
        evolution.
    """

    def __init__(
        self,
        traits: Iterable[CulturalTrait],
        *,
        baseline_bias: Optional[Mapping[str, float]] = None,
        learning_rate: float = 0.3,
    ) -> None:
        traits = list(traits)
        if not traits:
            raise ValueError("At least one cultural trait is required to simulate a culture.")
        if not 0.0 < learning_rate <= 1.0:
            raise ValueError("learning_rate must lie inside the (0, 1] interval.")

        self._traits: Dict[str, CulturalTrait] = {trait.name: trait for trait in traits}
        self._state: Dict[str, float] = {
            trait.name: trait.initial_prevalence for trait in traits
        }
        self._baseline_bias: Dict[str, float] = dict(baseline_bias or {})
        self.learning_rate = learning_rate
        self.environmental_factors: List[EnvironmentalFactor] = []

    @property
    def state(self) -> Dict[str, float]:
        """Return a copy of the current cultural state."""
        return dict(self._state)

    def set_environment(self, factors: Iterable[EnvironmentalFactor]) -> None:
        """Replace the active environmental factors."""
        self.environmental_factors = list(factors)

    def add_environmental_factor(self, factor: EnvironmentalFactor) -> None:
        """Append an environmental factor to the active list."""
        self.environmental_factors.append(factor)

    def _environment_bias(self, trait: CulturalTrait) -> float:
        return sum(factor.influence_for(trait.domain) for factor in self.environmental_factors)

    def simulate_step(
        self,
        *,
        interactions: Optional[Mapping[str, Mapping[str, float]]] = None,
        innovations: Optional[Mapping[str, float]] = None,
        external_bias: Optional[Mapping[str, float]] = None,
    ) -> Dict[str, float]:
        """Advance the culture by a single step and return the new state."""

        interactions = interactions or {}
        innovations = innovations or {}
        external_bias = external_bias or {}

        new_state: Dict[str, float] = {}
        for name, trait in self._traits.items():
            bias = self._baseline_bias.get(name, 0.0)
            bias += self._environment_bias(trait)
            bias += external_bias.get(name, 0.0)
            bias += innovations.get(name, 0.0)

            for other, weight in interactions.get(name, {}).items():
                if other not in self._state:
                    continue
                bias += weight * (self._state[other] - 0.5)

            target = _logistic(bias)
            updated = self._state[name] + self.learning_rate * (target - self._state[name])
            new_state[name] = _clamp_unit_interval(updated)

        self._state = new_state
        return self.state

    def simulate(
        self,
        steps: int,
        *,
        interactions: Optional[Mapping[str, Mapping[str, float]]] = None,
        innovations: Optional[Sequence[Mapping[str, float]]] = None,
        environment_timeline: Optional[Sequence[Iterable[EnvironmentalFactor]]] = None,
        external_biases: Optional[Sequence[Mapping[str, float]]] = None,
    ) -> List[Dict[str, float]]:
        """Simulate the culture for ``steps`` iterations and return the history."""

        if steps < 0:
            raise ValueError("steps must be non-negative.")

        history = [self.state]
        for index in range(steps):
            if environment_timeline is not None:
                self.set_environment(environment_timeline[index])

            innovation_step: Optional[Mapping[str, float]] = None
            if innovations is not None:
                innovation_step = innovations[index]

            bias_step: Optional[Mapping[str, float]] = None
            if external_biases is not None:
                bias_step = external_biases[index]

            history.append(
                self.simulate_step(
                    interactions=interactions,
                    innovations=innovation_step,
                    external_bias=bias_step,
                )
            )
        return history

    def cultural_distance(self, other_state: Mapping[str, float]) -> float:
        """Return the L1 distance to *other_state* for shared traits."""
        distance = 0.0
        for name, value in other_state.items():
            if name in self._state:
                distance += abs(self._state[name] - value)
        return distance

    def domain_focus(self) -> Dict[str, float]:
        """Return the average prevalence per domain."""
        totals: Dict[str, float] = {}
        counts: Dict[str, int] = {}
        for trait in self._traits.values():
            totals[trait.domain] = totals.get(trait.domain, 0.0) + self._state[trait.name]
            counts[trait.domain] = counts.get(trait.domain, 0) + 1
        return {domain: totals[domain] / counts[domain] for domain in totals}
