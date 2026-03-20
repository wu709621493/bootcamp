"""Variance summaries for factorial cell-count studies."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence


@dataclass(frozen=True)
class CellCountObservation:
    """A single cell-count reading from a factorial study."""

    researcher: str
    suspension_technique: str
    counter: str
    cell_count: float


__all__ = [
    "CellCountObservation",
    "summarize_cell_count_variance",
]


def _sample_variance(values: Sequence[float]) -> float:
    """Return the sample variance of ``values``.

    A single value has variance ``0.0`` in this helper to make grouped output
    convenient for balanced or sparse summaries.
    """

    if len(values) <= 1:
        return 0.0
    mean_value = sum(values) / len(values)
    return sum((value - mean_value) ** 2 for value in values) / (len(values) - 1)


def _normalize_observations(
    observations: Iterable[CellCountObservation | Mapping[str, object]],
) -> List[CellCountObservation]:
    normalized: List[CellCountObservation] = []
    for observation in observations:
        if isinstance(observation, CellCountObservation):
            normalized.append(observation)
            continue

        normalized.append(
            CellCountObservation(
                researcher=str(observation["researcher"]),
                suspension_technique=str(observation["suspension_technique"]),
                counter=str(observation["counter"]),
                cell_count=float(observation["cell_count"]),
            )
        )

    if not normalized:
        raise ValueError("At least one observation is required.")
    return normalized


def summarize_cell_count_variance(
    observations: Iterable[CellCountObservation | Mapping[str, object]],
) -> Dict[str, object]:
    """Summarize variance in a cell-count experiment.

    Parameters
    ----------
    observations:
        Iterable of observations containing ``researcher``,
        ``suspension_technique``, ``counter``, and ``cell_count`` fields.

    Returns
    -------
    dict
        A dictionary containing the grand mean, overall sample variance,
        grouped means and variances for each factor, and a main-effects-only
        sum-of-squares decomposition for balanced factorial designs.

    Notes
    -----
    The variance decomposition treats researcher, suspension technique, and
    counter as additive main effects. Any interaction structure is absorbed into
    the residual term. This means the function remains useful even when there is
    only one measurement per researcher/technique/counter combination.
    """

    normalized = _normalize_observations(observations)
    counts = [entry.cell_count for entry in normalized]
    grand_mean = sum(counts) / len(counts)

    grouped_values: Dict[str, Dict[str, List[float]]] = {
        "researcher": defaultdict(list),
        "suspension_technique": defaultdict(list),
        "counter": defaultdict(list),
    }

    for entry in normalized:
        grouped_values["researcher"][entry.researcher].append(entry.cell_count)
        grouped_values["suspension_technique"][entry.suspension_technique].append(entry.cell_count)
        grouped_values["counter"][entry.counter].append(entry.cell_count)

    grouped_stats: Dict[str, Dict[str, Dict[str, float]]] = {}
    for factor, factor_groups in grouped_values.items():
        grouped_stats[factor] = {
            name: {
                "count": len(values),
                "mean": sum(values) / len(values),
                "variance": _sample_variance(values),
            }
            for name, values in sorted(factor_groups.items())
        }

    researchers = sorted(grouped_values["researcher"])
    techniques = sorted(grouped_values["suspension_technique"])
    counters = sorted(grouped_values["counter"])

    technique_count = len(techniques)
    counter_count = len(counters)
    researcher_count = len(researchers)

    ss_total = sum((value - grand_mean) ** 2 for value in counts)
    ss_researcher = technique_count * counter_count * sum(
        (grouped_stats["researcher"][name]["mean"] - grand_mean) ** 2 for name in researchers
    )
    ss_suspension = researcher_count * counter_count * sum(
        (grouped_stats["suspension_technique"][name]["mean"] - grand_mean) ** 2 for name in techniques
    )
    ss_counter = researcher_count * technique_count * sum(
        (grouped_stats["counter"][name]["mean"] - grand_mean) ** 2 for name in counters
    )
    ss_residual = ss_total - ss_researcher - ss_suspension - ss_counter

    return {
        "observation_count": len(normalized),
        "grand_mean": grand_mean,
        "overall_variance": _sample_variance(counts),
        "by_factor": grouped_stats,
        "sum_of_squares": {
            "total": ss_total,
            "researcher": ss_researcher,
            "suspension_technique": ss_suspension,
            "counter": ss_counter,
            "residual": ss_residual,
        },
        "variance_fraction": {
            "researcher": ss_researcher / ss_total if ss_total else 0.0,
            "suspension_technique": ss_suspension / ss_total if ss_total else 0.0,
            "counter": ss_counter / ss_total if ss_total else 0.0,
            "residual": ss_residual / ss_total if ss_total else 0.0,
        },
    }
