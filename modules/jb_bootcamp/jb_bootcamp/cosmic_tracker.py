"""Utilities for exploring string-theory inspired cosmic observation targets."""

from __future__ import annotations

import csv
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

__all__ = [
    "CosmicCandidate",
    "load_candidates",
    "filter_candidates",
    "summarize_by_instrumentation",
    "search_structures",
]

_DATA_FILENAME = "string_theory_observational_candidates.csv"
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_DATA_PATH = _PROJECT_ROOT / "data" / _DATA_FILENAME


@dataclass(frozen=True)
class CosmicCandidate:
    """Record describing a hypothetical cosmic observation campaign."""

    candidate: str
    signature_type: str
    measurement_goal: str
    instrumentation: str
    mission_context: str
    notes: str


def load_candidates(path: str | Path | None = None) -> tuple[CosmicCandidate, ...]:
    """Return the dataset of observation candidates as :class:`CosmicCandidate` objects.

    Parameters
    ----------
    path:
        Optional override for the CSV file to read. ``path`` may point directly
        to a file or to a directory containing
        ``string_theory_observational_candidates.csv``.

    Raises
    ------
    FileNotFoundError
        If ``path`` (or the inferred default location) does not exist.
    ValueError
        If the CSV does not provide the required column headers.
    """

    csv_path = _resolve_dataset_path(path)

    with csv_path.open(newline="", encoding="utf8") as handle:
        reader = csv.DictReader(handle)
        required_fields = tuple(CosmicCandidate.__annotations__.keys())
        if reader.fieldnames is None:
            raise ValueError("Dataset is missing a header row.")

        missing = [field for field in required_fields if field not in reader.fieldnames]
        if missing:
            missing_fields = ", ".join(sorted(missing))
            raise ValueError(f"Dataset missing required columns: {missing_fields}.")

        rows = [
            CosmicCandidate(
                **{field: row[field].strip() for field in required_fields}
            )
            for row in reader
        ]

    return tuple(rows)


def filter_candidates(
    candidates: Sequence[CosmicCandidate],
    *,
    signature_type: str | Iterable[str] | None = None,
    instrumentation: str | Iterable[str] | None = None,
    mission_context: str | Iterable[str] | None = None,
    keyword: str | Iterable[str] | None = None,
) -> tuple[CosmicCandidate, ...]:
    """Filter ``candidates`` according to mission attributes.

    Each filter argument accepts either a single string or an iterable of
    strings.  Comparisons are case-insensitive and require an exact match
    against the corresponding field.

    The ``keyword`` argument performs a broad search across *all* text fields
    and checks whether any of the provided keywords appears as a substring.
    """

    signature_filter = _normalise_criteria(signature_type)
    instrumentation_filter = _normalise_criteria(instrumentation)
    mission_filter = _normalise_criteria(mission_context)
    keywords = _normalise_keywords(keyword)

    def matches(candidate: CosmicCandidate) -> bool:
        if signature_filter and candidate.signature_type.casefold() not in signature_filter:
            return False
        if (
            instrumentation_filter
            and candidate.instrumentation.casefold() not in instrumentation_filter
        ):
            return False
        if mission_filter and candidate.mission_context.casefold() not in mission_filter:
            return False
        if keywords and not _contains_keyword(candidate, keywords):
            return False
        return True

    return tuple(candidate for candidate in candidates if matches(candidate))


def summarize_by_instrumentation(
    candidates: Sequence[CosmicCandidate],
) -> Mapping[str, tuple[CosmicCandidate, ...]]:
    """Group candidates by their required instrumentation.

    The returned mapping preserves the order in which instrumentation entries
    first appear in ``candidates``.
    """

    grouped: OrderedDict[str, list[CosmicCandidate]] = OrderedDict()
    for candidate in candidates:
        grouped.setdefault(candidate.instrumentation, []).append(candidate)

    return {key: tuple(value) for key, value in grouped.items()}


def search_structures(
    candidates: Sequence[CosmicCandidate],
    *,
    keywords: str | Iterable[str] | None = None,
) -> tuple[CosmicCandidate, ...]:
    """Return candidates associated with astronomical structures.

    Parameters
    ----------
    candidates:
        Iterable of :class:`CosmicCandidate` records to search through.
    keywords:
        Optional override for the substrings that identify a structure.
        When omitted, defaults to searching for both "structure" and
        "structures".  Matching is performed case-insensitively across all
        text fields of each candidate.

    Returns
    -------
    tuple[CosmicCandidate, ...]
        Candidates where at least one keyword appears in any field.

    Raises
    ------
    ValueError
        If ``keywords`` is provided but does not contain any non-empty
        strings.
    """

    default_keywords = ("structure", "structures")
    normalised_keywords = _normalise_keywords(keywords or default_keywords)
    if not normalised_keywords:
        raise ValueError("At least one keyword is required to search structures.")

    return tuple(
        candidate
        for candidate in candidates
        if _contains_keyword(candidate, normalised_keywords)
    )


def _resolve_dataset_path(path: str | Path | None) -> Path:
    if path is None:
        csv_path = _DEFAULT_DATA_PATH
    else:
        csv_path = Path(path)
        if csv_path.is_dir():
            candidate_path = csv_path / _DATA_FILENAME
            if candidate_path.exists():
                csv_path = candidate_path
            else:
                raise FileNotFoundError(
                    f"{csv_path} does not contain {_DATA_FILENAME!r}."
                )

    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    return csv_path


def _normalise_criteria(value: str | Iterable[str] | None) -> set[str]:
    """Return a case-folded set of ``value`` while validating the input."""

    if value is None:
        return set()
    if isinstance(value, str):
        return {value.casefold()}

    try:
        iterator = iter(value)
    except TypeError as exc:  # pragma: no cover - defensive guard
        raise TypeError("Filter criteria must be a string or iterable of strings.") from exc

    normalised: set[str] = set()
    for item in iterator:
        if not isinstance(item, str):
            raise TypeError("Filter criteria must only contain strings.")
        normalised.add(item.casefold())
    return normalised


def _normalise_keywords(value: str | Iterable[str] | None) -> tuple[str, ...]:
    """Return a tuple of normalised keywords while validating the input."""

    if value is None:
        return ()
    if isinstance(value, str):
        values = [value]
    else:
        try:
            values = list(value)
        except TypeError as exc:  # pragma: no cover - defensive guard
            raise TypeError("Keywords must be provided as a string or iterable of strings.") from exc

    normalised: list[str] = []
    for item in values:
        if not isinstance(item, str):
            raise TypeError("Keywords must only contain strings.")
        if item:
            normalised.append(item.casefold())
    return tuple(normalised)


def _contains_keyword(candidate: CosmicCandidate, keywords: Iterable[str]) -> bool:
    haystacks = (
        candidate.candidate,
        candidate.signature_type,
        candidate.measurement_goal,
        candidate.instrumentation,
        candidate.mission_context,
        candidate.notes,
    )
    normalised_haystacks = [field.casefold() for field in haystacks]
    return any(keyword in field for field in normalised_haystacks for keyword in keywords)
