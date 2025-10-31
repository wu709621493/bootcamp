"""Statistical utilities related to Poisson processes."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple, Union


Number = Union[int, float]


@dataclass(frozen=True)
class QuantizedPoissonResult:
    """Container for the results of Poisson time quantisation."""

    times: Tuple[float, ...]
    counts: Tuple[int, ...]
    bin_edges: Tuple[float, ...]

    def as_tuple(self) -> Tuple[Tuple[float, ...], Tuple[int, ...], Tuple[float, ...]]:
        """Return the quantisation results as a plain tuple."""

        return self.times, self.counts, self.bin_edges


def _validate_bin_width(bin_width: Number) -> float:
    width = float(bin_width)
    if width <= 0:
        raise ValueError("bin_width must be positive.")
    return width


def _resolve_time_window(spike_times: Sequence[float], start: Optional[Number], end: Optional[Number]) -> Tuple[float, float]:
    if not spike_times and (start is None or end is None):
        raise ValueError("start and end must be supplied when spike_times is empty.")

    if start is None:
        start = min(spike_times)
    if end is None:
        end = max(spike_times)

    start_f = float(start)
    end_f = float(end)
    if end_f <= start_f:
        raise ValueError("end must be greater than start.")

    return start_f, end_f


def _prepare_rng(random_state: Optional[Union[random.Random, int]]) -> random.Random:
    if isinstance(random_state, random.Random):
        return random_state

    rng = random.Random()
    if random_state is not None:
        rng.seed(random_state)
    return rng


def _poisson_sample(lam: float, rng: random.Random) -> int:
    if lam < 0:
        raise ValueError("Poisson rate must be non-negative.")
    if lam == 0:
        return 0

    # Knuth's algorithm for sampling from a Poisson distribution.
    threshold = math.exp(-lam)
    k = 0
    product = 1.0
    while product > threshold:
        k += 1
        product *= rng.random()
    return k - 1


def _to_float_sequence(values: Sequence[Number]) -> List[float]:
    floats: List[float] = []
    for value in values:
        f_value = float(value)
        if not math.isfinite(f_value):
            raise ValueError("spike_times must contain finite values.")
        floats.append(f_value)
    return floats


def quantize_time_by_poisson(
    spike_times: Sequence[Number],
    bin_width: Number,
    *,
    start: Optional[Number] = None,
    end: Optional[Number] = None,
    rate: Optional[Number] = None,
    random_state: Optional[Union[random.Random, int]] = None,
) -> QuantizedPoissonResult:
    """Quantise time into bins with Poisson-distributed occupancies.

    Parameters
    ----------
    spike_times:
        One-dimensional array-like of event times.  These may be spike
        times from a fly photoreceptor, calcium transient peaks, or any
        other timestamped events that can be modelled by a homogeneous
        Poisson process.
    bin_width:
        Width of each time bin.  Must be strictly positive.
    start, end:
        Optional explicit start and end of the time window.  If omitted
        they are inferred from ``spike_times``.  When ``spike_times`` is
        empty both ``start`` and ``end`` must be provided.
    rate:
        Optional expected event rate (events per unit time).  When not
        provided it is estimated from ``spike_times`` as ``N / T``.
    random_state:
        Seed or :class:`random.Random` controlling the random sampling
        from the Poisson distribution.

    Returns
    -------
    QuantizedPoissonResult
        Dataclass containing the synthetic event times (repeated bin
        centres), the counts for each bin, and the bin edges used for
        quantisation.

    Notes
    -----
    This function constructs a homogeneous Poisson model for the events
    and returns a synthetic spike train sampled from that model.  The
    output is often useful when constructing null models to compare
    against recordings from visual neurons in the fruit fly, where spike
    trains are frequently approximated as Poisson processes.
    """

    spike_array = _to_float_sequence(spike_times)

    width = _validate_bin_width(bin_width)
    start_f, end_f = _resolve_time_window(spike_array, start, end)

    if rate is None:
        duration = end_f - start_f
        if duration <= 0:
            raise ValueError("Cannot infer rate because time window is non-positive.")
        if spike_array:
            rate_value = len(spike_array) / duration
        else:
            rate_value = 0.0
    else:
        rate_value = float(rate)

    if rate_value < 0:
        raise ValueError("rate must be non-negative.")

    rng = _prepare_rng(random_state)

    # Build bin edges that cover the requested interval
    num_bins = max(1, int(math.ceil((end_f - start_f) / width)))
    bin_edges: List[float] = [start_f + i * width for i in range(num_bins + 1)]
    if bin_edges[-1] < end_f:
        bin_edges.append(bin_edges[-1] + width)

    expected = rate_value * width
    counts: List[int] = [_poisson_sample(expected, rng) for _ in range(len(bin_edges) - 1)]

    bin_centres = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(bin_edges) - 1)]
    quantized_times: List[float] = []
    for centre, count in zip(bin_centres, counts):
        quantized_times.extend([centre] * count)

    return QuantizedPoissonResult(
        times=tuple(quantized_times),
        counts=tuple(counts),
        bin_edges=tuple(bin_edges),
    )
