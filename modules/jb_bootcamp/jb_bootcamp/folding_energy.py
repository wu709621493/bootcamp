"""Imaginary potential energy landscape for an infinite sequence fly.

This module provides a lightweight mathematical toy model that encodes the
"imaginary" potential energy barriers encountered as an abstract, infinitely
folded creature---the so-called *sequence fly*---progresses through deeper
levels of folding.  The goal is not to mimic any physical process, but rather
to offer a reproducible way of generating complex numbers whose magnitudes and
phases follow a spiral decay reminiscent of increasingly delicate folds.

The model is intentionally deterministic so that experiments and plots created
from it can be reproduced exactly.  By adjusting a handful of parameters the
user can control how quickly the barrier magnitudes decay, how tightly the
spiral winds, and how much imaginary "lift" each fold accumulates.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import List, Sequence


@dataclass(frozen=True)
class InfiniteSequenceFly:
    """Generator for folding energy barriers of an infinite sequence fly.

    Parameters
    ----------
    base_energy:
        Initial barrier height for the zeroth folding level.  The value must be
        strictly positive so that subsequent levels have a well-defined scale.
    fold_ratio:
        Exponential growth factor applied to the logarithmic measure of the
        folding depth.  Values slightly above one produce gentle growth before
        the exponential damping takes over, while larger values introduce more
        dramatic early barriers.
    damping:
        Exponential damping applied per folding level.  This controls how fast
        the magnitude of the barriers shrinks as the folding depth increases.
    torsion:
        Strength of the imaginary component added to the spiral response.  The
        value can be any finite real number; positive values tilt the spiral
        upward in the complex plane while negative values mirror it.
    pitch:
        Phase advance per square root of the folding level.  This determines how
        tightly the spiral winds as deeper folds are considered.
    """

    base_energy: float = 1.0
    fold_ratio: float = 1.35
    damping: float = 0.55
    torsion: float = 0.8
    pitch: float = 0.75

    def __post_init__(self) -> None:
        if self.base_energy <= 0.0:
            raise ValueError("base_energy must be strictly positive.")
        if self.fold_ratio <= 0.0:
            raise ValueError("fold_ratio must be strictly positive.")
        if self.damping <= 0.0:
            raise ValueError("damping must be strictly positive.")
        if not math.isfinite(self.torsion):
            raise ValueError("torsion must be a finite real number.")
        if self.pitch < 0.0:
            raise ValueError("pitch must be non-negative.")

    def barrier(self, level: int) -> complex:
        """Return the complex barrier encountered at *level* of folding.

        The implementation models the barrier as a decaying logarithmic spiral
        that also accumulates a level-dependent imaginary tilt.  Higher levels
        therefore continue to shrink in magnitude while their complex phase
        continues to advance, capturing the intuition of ever more fragile
        layers of folding.
        """

        if level < 0:
            raise ValueError("level must be non-negative.")

        if level == 0:
            return complex(self.base_energy, 0.0)

        fold_progress = math.log1p(level)
        amplitude = self.base_energy * math.exp(
            fold_progress * math.log(self.fold_ratio) - self.damping * level
        )
        phase = self.pitch * math.sqrt(level)
        spiral = amplitude * complex(math.cos(phase), math.sin(phase))
        twist = complex(1.0, self.torsion * math.tanh(math.sqrt(level)))
        return spiral * twist

    def landscape(self, levels: int) -> List[complex]:
        """Return the barrier sequence for the first *levels* folds."""

        if levels < 0:
            raise ValueError("levels must be non-negative.")
        return [self.barrier(level) for level in range(levels)]


def imaginary_potential_barriers(
    levels: int,
    *,
    base_energy: float = 1.0,
    fold_ratio: float = 1.35,
    damping: float = 0.55,
    torsion: float = 0.8,
    pitch: float = 0.75,
) -> Sequence[complex]:
    """Convenience wrapper for generating an energy landscape.

    Parameters mirror :class:`InfiniteSequenceFly` so users can obtain the same
    results without manually instantiating the class.  The returned sequence is
    a list of complex numbers whose magnitudes monotonically decrease as the
    folding level increases, while the phase advances and the imaginary
    component gradually saturates.
    """

    fly = InfiniteSequenceFly(
        base_energy=base_energy,
        fold_ratio=fold_ratio,
        damping=damping,
        torsion=torsion,
        pitch=pitch,
    )
    return fly.landscape(levels)

