"""Tests for the alien culture simulation module."""
from __future__ import annotations

import pathlib
import sys

import pytest


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


from jb_bootcamp.alien_culture import (
    AlienCulture,
    CulturalTrait,
    EnvironmentalFactor,
)


def test_simulate_step_with_environment_and_interactions():
    traits = [
        CulturalTrait("bioluminescent_art", "aesthetic", 0.3),
        CulturalTrait("collective_memory", "knowledge", 0.4),
    ]
    culture = AlienCulture(traits, baseline_bias={"collective_memory": 0.1}, learning_rate=0.5)
    culture.set_environment(
        [EnvironmentalFactor("deep_ocean", weight=1.1, effects={"aesthetic": 0.5})]
    )
    interactions = {"collective_memory": {"bioluminescent_art": 1.0}}
    innovations = {"bioluminescent_art": 0.2}

    new_state = culture.simulate_step(interactions=interactions, innovations=innovations)

    assert new_state["bioluminescent_art"] == pytest.approx(0.4896, abs=1e-3)
    assert new_state["collective_memory"] == pytest.approx(0.4375, abs=1e-3)


def test_simulation_history_and_domain_focus():
    traits = [
        CulturalTrait("sky_chants", "ritual", 0.6),
        CulturalTrait("geomancy", "knowledge", 0.2),
    ]
    culture = AlienCulture(traits, learning_rate=0.3)

    environments = [
        [EnvironmentalFactor("solar_flare", weight=0.4, effects={"ritual": -0.5})],
        [EnvironmentalFactor("tidal_lock", weight=0.8, effects={"ritual": 0.6})],
    ]
    innovations = [
        {"geomancy": 0.3},
        {"geomancy": -0.1},
    ]

    history = culture.simulate(
        2,
        interactions=None,
        innovations=innovations,
        environment_timeline=environments,
    )

    assert len(history) == 3
    assert history[0]["geomancy"] == pytest.approx(0.2)
    assert history[-1]["geomancy"] > history[0]["geomancy"]

    domain_focus = culture.domain_focus()
    assert set(domain_focus) == {"ritual", "knowledge"}
    assert domain_focus["knowledge"] == pytest.approx(culture.state["geomancy"])


def test_trait_validation_and_cultural_distance():
    with pytest.raises(ValueError):
        CulturalTrait("", "ritual", 0.3)
    with pytest.raises(ValueError):
        CulturalTrait("dream_cycle", "", 0.3)
    with pytest.raises(ValueError):
        CulturalTrait("dream_cycle", "ritual", 1.3)

    culture = AlienCulture([CulturalTrait("aural_cartography", "knowledge", 0.5)])
    baseline_state = culture.state
    assert culture.cultural_distance(baseline_state) == pytest.approx(0.0)

    target_state = {"aural_cartography": 0.9}
    culture.simulate_step(innovations={"aural_cartography": 0.6})
    assert culture.cultural_distance(target_state) == pytest.approx(
        abs(culture.state["aural_cartography"] - 0.9)
    )
