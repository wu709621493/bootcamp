"""Tests for Poisson time quantisation utilities."""

import pathlib
import random
import sys

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "modules"))

from jb_bootcamp.jb_bootcamp.poisson import quantize_time_by_poisson


def test_quantize_time_reproducible_with_seed():
    spike_times = [0.0, 0.5, 1.0, 1.5]

    result_a = quantize_time_by_poisson(spike_times, bin_width=0.5, random_state=37)
    result_b = quantize_time_by_poisson(spike_times, bin_width=0.5, random_state=37)

    assert result_a.counts == result_b.counts
    assert result_a.times == result_b.times
    assert result_a.bin_edges == result_b.bin_edges


def test_quantize_time_respects_custom_window():
    result = quantize_time_by_poisson([], bin_width=1.0, start=0.0, end=5.0, rate=0.25, random_state=12)

    assert result.bin_edges[0] == pytest.approx(0.0)
    assert result.bin_edges[-1] >= 5.0
    assert len(result.counts) == len(result.bin_edges) - 1


def test_quantize_time_with_random_instance():
    rng = random.Random(5)
    result = quantize_time_by_poisson([0.0, 1.0], bin_width=0.5, random_state=rng)

    # Ensure we used the provided RNG by checking determinism when reused.
    rng.seed(5)
    result_again = quantize_time_by_poisson([0.0, 1.0], bin_width=0.5, random_state=rng)

    assert result.counts == result_again.counts


@pytest.mark.parametrize(
    "spike_times, bin_width, kwargs",
    [
        ([0.0, 0.5], 0.0, {}),
        ([0.0, 0.5], -1.0, {}),
        ([0.0, 0.5], 0.5, {"rate": -0.1}),
        ([], 1.0, {"start": 1.0, "end": 0.0}),
        ([], 1.0, {"rate": 1.0}),
    ],
)
def test_invalid_parameters_raise_value_error(spike_times, bin_width, kwargs):
    with pytest.raises(ValueError):
        quantize_time_by_poisson(spike_times, bin_width, **kwargs)
