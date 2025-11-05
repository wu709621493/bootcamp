"""Tests for the imaginary folding energy landscape model."""

from __future__ import annotations

import math

import pytest

from jb_bootcamp.folding_energy import (
    InfiniteSequenceFly,
    imaginary_potential_barriers,
)


def test_zero_level_barrier_matches_base_energy() -> None:
    fly = InfiniteSequenceFly(base_energy=2.5)
    barrier = fly.barrier(0)
    assert barrier.real == pytest.approx(2.5)
    assert barrier.imag == pytest.approx(0.0)


def test_landscape_is_monotonic_in_magnitude() -> None:
    fly = InfiniteSequenceFly()
    landscape = fly.landscape(6)
    magnitudes = [abs(value) for value in landscape]
    assert all(a >= b for a, b in zip(magnitudes, magnitudes[1:]))


def test_wrapper_matches_class_landscape() -> None:
    params = dict(base_energy=1.3, fold_ratio=1.4, damping=0.6, torsion=0.7, pitch=0.5)
    fly = InfiniteSequenceFly(**params)
    assert imaginary_potential_barriers(5, **params) == fly.landscape(5)


def test_invalid_inputs_raise_value_error() -> None:
    fly = InfiniteSequenceFly()
    with pytest.raises(ValueError):
        fly.barrier(-1)
    with pytest.raises(ValueError):
        fly.landscape(-3)
    with pytest.raises(ValueError):
        InfiniteSequenceFly(base_energy=-1.0)
    with pytest.raises(ValueError):
        InfiniteSequenceFly(fold_ratio=0.0)
    with pytest.raises(ValueError):
        InfiniteSequenceFly(damping=0.0)
    with pytest.raises(ValueError):
        InfiniteSequenceFly(torsion=math.inf)
    with pytest.raises(ValueError):
        InfiniteSequenceFly(pitch=-0.1)

