"""Utilities for lightweight ethical compliance evaluations.

The module is intentionally pragmatic: it provides a small helper that can
ingest loosely-structured ethical review information (booleans, numeric scores
expressed as fractions or percentages, textual labels, or nested dictionaries)
and distil it into a consistent representation.  The helper is designed for
teaching exercises where students explore how to reason about competing
principles rather than for production governance software.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, MutableSequence, Sequence

__all__ = ["EthicEvaluation", "ethic_evaluation"]


@dataclass(frozen=True)
class EthicEvaluation:
    """Normalised ethical assessment for a proposal or decision.

    Attributes
    ----------
    overall_score:
        Weighted score between zero and one representing the final assessment.
    status:
        Human-readable label that summarises the outcome.  The helper returns
        one of ``"compliant"``, ``"needs_review"``, or ``"non_compliant"``.
    principle_scores:
        Mapping from principle name to the normalised score assigned to that
        principle.
    concerns:
        Tuple of explanatory notes or concerns surfaced during evaluation.
    summary:
        Concise textual description of the outcome that can be presented to
        students when discussing the result.
    """

    overall_score: float
    status: str
    principle_scores: Mapping[str, float]
    concerns: tuple[str, ...]
    summary: str


_STATUS_MAP = {
    "compliant": 1.0,
    "fully compliant": 1.0,
    "approved": 1.0,
    "aligned": 0.9,
    "support": 0.85,
    "meets": 0.8,
    "meets requirements": 0.8,
    "partial": 0.6,
    "partially compliant": 0.6,
    "unclear": 0.5,
    "requires clarification": 0.5,
    "needs review": 0.5,
    "mitigated": 0.5,
    "minor concern": 0.4,
    "concern": 0.35,
    "significant concern": 0.25,
    "at risk": 0.2,
    "breach": 0.0,
    "violation": 0.0,
    "non compliant": 0.0,
    "non-compliant": 0.0,
    "rejected": 0.0,
    "prohibited": 0.0,
    "fail": 0.0,
}


def _clamp(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


def _normalise_concerns(raw: object) -> Iterable[str]:
    if raw is None:
        return ()
    if isinstance(raw, str):
        text = raw.strip()
        return (text,) if text else ()
    if isinstance(raw, Mapping):
        concerns: list[str] = []
        for value in raw.values():
            concerns.extend(_normalise_concerns(value))
        return tuple(concerns)
    if isinstance(raw, Sequence) and not isinstance(raw, (bytes, str)):
        concerns: list[str] = []
        for value in raw:
            concerns.extend(_normalise_concerns(value))
        return tuple(concerns)
    return (str(raw),)


def _score_from_status(value: str) -> float:
    normalised = value.strip().lower()
    if normalised in _STATUS_MAP:
        return _STATUS_MAP[normalised]
    raise ValueError(f"Unknown ethical status label: {value!r}.")


def _coerce_score(raw: object) -> float:
    if isinstance(raw, bool):
        return 1.0 if raw else 0.0
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        number = float(raw)
        if number > 1.0 and number <= 100.0:
            number /= 100.0
        return _clamp(number)
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            raise ValueError("Empty string cannot be interpreted as an ethical score.")
        lowered = text.lower()
        if lowered in _STATUS_MAP:
            return _STATUS_MAP[lowered]
        try:
            value = float(text)
        except ValueError as exc:
            raise ValueError(f"Cannot interpret ethical score from {raw!r}.") from exc
        if value > 1.0 and value <= 100.0:
            value /= 100.0
        return _clamp(value)
    if isinstance(raw, Mapping):
        scores: MutableSequence[float] = []
        for key, value in raw.items():
            key_lower = str(key).strip().lower()
            if key_lower in {"score", "value", "rating", "weight", "level"}:
                scores.append(_coerce_score(value))
            elif key_lower in {"status", "assessment", "label"}:
                if isinstance(value, str):
                    scores.append(_score_from_status(value))
                else:
                    scores.append(_coerce_score(value))
            elif key_lower in {"compliant", "compliance"}:
                scores.append(_coerce_score(value))
        if scores:
            return sum(scores) / len(scores)
        # If the mapping did not contain recognised keys fall back to its values.
        values = list(raw.values())
        if not values:
            raise ValueError("Cannot interpret score from empty mapping.")
        return sum(_coerce_score(value) for value in values) / len(values)
    if isinstance(raw, Sequence) and not isinstance(raw, (bytes, str)):
        if not raw:
            raise ValueError("Cannot interpret score from an empty sequence.")
        return sum(_coerce_score(value) for value in raw) / len(raw)
    raise TypeError(f"Unsupported type for ethical score normalisation: {type(raw)!r}.")


def _normalise_entry(raw: object) -> tuple[float, tuple[str, ...]]:
    if isinstance(raw, Mapping):
        concerns: list[str] = []
        if "concerns" in raw:
            concerns.extend(_normalise_concerns(raw["concerns"]))
        for key, value in raw.items():
            key_lower = str(key).strip().lower()
            if key_lower in {"notes", "rationale", "comment", "summary", "issue", "issues"}:
                concerns.extend(_normalise_concerns(value))
        score = _coerce_score(raw)
        return score, tuple(concerns)
    score = _coerce_score(raw)
    return score, ()


def ethic_evaluation(
    principles: Mapping[str, object],
    *,
    weights: Mapping[str, float] | None = None,
    review_threshold: float = 0.7,
    compliance_threshold: float = 0.85,
) -> EthicEvaluation:
    """Evaluate ethical alignment for ``principles``.

    Parameters
    ----------
    principles:
        Mapping of principle name to an assessment.  Assessments are flexible
        and may be booleans, numeric scores, descriptive strings, sequences of
        scores, or dictionaries containing keys such as ``"score"`` or
        ``"status"``.  Additional keys like ``"concerns"`` or ``"notes``
        contribute contextual information to the final result.
    weights:
        Optional mapping from principle name to a non-negative numeric weight
        used when computing the overall score.  Principles not listed default
        to a unit weight.
    review_threshold:
        Minimum overall score required to avoid the ``"needs_review"`` status.
    compliance_threshold:
        Minimum score required for the ``"compliant"`` status.  Values equal or
        above ``compliance_threshold`` yield ``"compliant"``; values between the
        thresholds yield ``"needs_review"``; values below ``review_threshold``
        yield ``"non_compliant"``.
    """

    if not principles:
        raise ValueError("At least one ethical principle must be provided for evaluation.")

    weights = weights or {}
    scores: dict[str, float] = {}
    concerns: list[str] = []

    for principle, raw in principles.items():
        name = str(principle)
        score, entry_concerns = _normalise_entry(raw)
        scores[name] = score
        concerns.extend(entry_concerns)

    total_weight = 0.0
    weighted_score = 0.0
    for principle, score in scores.items():
        weight = float(weights.get(principle, 1.0))
        if weight < 0.0:
            raise ValueError("Weights must be non-negative.")
        if weight == 0.0:
            continue
        weighted_score += score * weight
        total_weight += weight

    if total_weight == 0.0:
        raise ValueError("Total weight for ethical evaluation must be positive.")

    overall = weighted_score / total_weight

    if overall >= compliance_threshold:
        status = "compliant"
    elif overall >= review_threshold:
        status = "needs_review"
    else:
        status = "non_compliant"

    unique_concerns = []
    seen = set()
    for item in concerns:
        if not item:
            continue
        if item not in seen:
            unique_concerns.append(item)
            seen.add(item)

    summary_parts = [
        f"Overall ethical score {overall:.2f} ({status.replace('_', ' ')}).",
        f"Evaluated {len(scores)} principles.",
    ]
    if unique_concerns:
        summary_parts.append("Concerns: " + "; ".join(unique_concerns))

    return EthicEvaluation(
        overall_score=overall,
        status=status,
        principle_scores=scores,
        concerns=tuple(unique_concerns),
        summary=" ".join(summary_parts),
    )

