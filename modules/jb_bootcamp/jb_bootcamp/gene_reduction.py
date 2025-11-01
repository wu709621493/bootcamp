"""Tools for simulating gene length and copy number reduction.

This module provides lightweight utilities for bootcamp participants who want
simple, deterministic simulations of gene attrition experiments.  The
functionality is intentionally straightforward so it can be used in a teaching
setting without extra dependencies.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence


DEFAULT_AMINO_ACIDS: Sequence[str] = (
    "A", "C", "D", "E", "F", "G", "H", "K", "L"
)
"""Nine amino-acid symbols that can populate the Sudoku-like board."""


def _pattern(row: int, col: int) -> int:
    """Return the canonical Sudoku pattern index for the given cell."""

    return (3 * (row % 3) + row // 3 + col) % 9


def _shuffle(values: Sequence[int], rng: random.Random) -> List[int]:
    """Return a shuffled copy of ``values`` using ``rng`` for reproducibility."""

    values = list(values)
    rng.shuffle(values)
    return values


def generate_amino_acid_sudoku(
    amino_acids: Sequence[str] | None = None,
    seed: int | None = None,
) -> List[List[str]]:
    """Generate a filled Sudoku board populated by amino-acid symbols.

    The routine uses the standard pattern/shuffle recipe for constructing a
    valid Sudoku grid.  Each row, column, and 3×3 sub-grid contains each amino
    acid exactly once.

    Parameters
    ----------
    amino_acids:
        Iterable of nine distinct symbols used to populate the board.
        If omitted, :data:`DEFAULT_AMINO_ACIDS` is used.
    seed:
        Optional random seed that ensures deterministic board construction.

    Returns
    -------
    list of list of str
        A 9×9 grid of amino-acid symbols.

    Raises
    ------
    ValueError
        If ``amino_acids`` does not contain exactly nine distinct entries.
    """

    if amino_acids is None:
        amino_acids = DEFAULT_AMINO_ACIDS

    amino_acids = tuple(amino_acids)
    if len(amino_acids) != 9 or len(set(amino_acids)) != 9:
        raise ValueError("amino_acids must contain nine distinct symbols")

    rng = random.Random(seed)
    rows = [g * 3 + r for g in _shuffle(range(3), rng) for r in _shuffle(range(3), rng)]
    cols = [g * 3 + c for g in _shuffle(range(3), rng) for c in _shuffle(range(3), rng)]
    symbols = list(amino_acids)
    rng.shuffle(symbols)

    board = [[symbols[_pattern(r, c)] for c in cols] for r in rows]
    return board


@dataclass
class ReductionStep:
    """Container describing a single gene reduction event."""

    removed_gene_index: int
    removed_bases: int
    remaining_lengths: List[int]


def simulate_gene_reduction(
    initial_lengths: Iterable[int],
    fraction_removed: float,
    steps: int,
    seed: int | None = None,
) -> List[ReductionStep]:
    """Simulate successive gene-length reductions.

    Parameters
    ----------
    initial_lengths:
        Iterable of positive integers describing gene lengths in bases.
    fraction_removed:
        Fraction of the selected gene removed during each step.  The simulator
        always removes at least one base.
    steps:
        Maximum number of reduction steps to perform.
    seed:
        Optional random seed for reproducibility.

    Returns
    -------
    list of :class:`ReductionStep`
        Chronological record of the simulation.  Once all genes have been
        depleted, the simulation stops even if ``steps`` has not been reached.

    Raises
    ------
    ValueError
        If ``fraction_removed`` is not between 0 and 1 (exclusive).
    """

    if not 0 < fraction_removed < 1:
        raise ValueError("fraction_removed must be between 0 and 1")

    lengths = [int(value) for value in initial_lengths if int(value) > 0]
    rng = random.Random(seed)
    history: List[ReductionStep] = []

    for _ in range(steps):
        if not lengths:
            break

        gene_index = rng.randrange(len(lengths))
        current_length = lengths[gene_index]
        removed = max(1, int(round(current_length * fraction_removed)))
        removed = min(removed, current_length)
        lengths[gene_index] -= removed

        if lengths[gene_index] == 0:
            lengths.pop(gene_index)

        history.append(
            ReductionStep(
                removed_gene_index=gene_index,
                removed_bases=removed,
                remaining_lengths=list(lengths),
            )
        )

    return history


def summarize_history(history: Sequence[ReductionStep]) -> dict[str, float]:
    """Summarize a gene-reduction history with simple aggregate metrics."""

    if not history:
        return {"steps": 0, "bases_removed": 0.0, "mean_remaining": 0.0}

    total_removed = sum(step.removed_bases for step in history)
    if history[-1].remaining_lengths:
        mean_remaining = sum(history[-1].remaining_lengths) / len(history[-1].remaining_lengths)
    else:
        mean_remaining = 0.0

    return {
        "steps": float(len(history)),
        "bases_removed": float(total_removed),
        "mean_remaining": float(mean_remaining),
    }
