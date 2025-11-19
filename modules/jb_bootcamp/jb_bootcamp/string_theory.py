"""Utilities for summarising the string theory observational dataset."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA = REPO_ROOT / "data" / "string_theory_observational_candidates.csv"

_CSV_FIELDS = (
    "candidate",
    "signature_type",
    "measurement_goal",
    "instrumentation",
    "mission_context",
    "notes",
)


@dataclass(frozen=True)
class Candidate:
    """Representation of a single observational proposal."""

    candidate: str
    signature_type: str
    measurement_goal: str
    instrumentation: str
    mission_context: str
    notes: str


@dataclass
class _SignatureBucket:
    count: int = 0
    instruments: set[str] = field(default_factory=set)
    missions: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class SignatureSummary:
    """Aggregate information for a signature type."""

    signature_type: str
    count: int
    instruments: tuple[str, ...]
    missions: tuple[str, ...]


def _clean(value: str | None) -> str:
    return (value or "").strip()


def load_candidates(path: Path | str | None = None) -> list[Candidate]:
    """Load candidates from ``path`` or the default CSV."""

    data_path = Path(path) if path is not None else DEFAULT_DATA
    with data_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        missing = [field for field in _CSV_FIELDS if field not in fieldnames]
        if missing:
            raise ValueError(f"Missing expected columns in dataset: {missing!r}")
        rows: list[Candidate] = []
        for raw in reader:
            cleaned = {field: _clean(raw.get(field)) for field in _CSV_FIELDS}
            rows.append(Candidate(**cleaned))
    return rows


def summarize_by_signature(candidates: Iterable[Candidate]) -> dict[str, SignatureSummary]:
    """Group ``candidates`` by signature type with instrument + mission lists."""

    buckets: defaultdict[str, _SignatureBucket] = defaultdict(_SignatureBucket)
    for entry in candidates:
        bucket = buckets[entry.signature_type]
        bucket.count += 1
        bucket.instruments.add(entry.instrumentation)
        bucket.missions.add(entry.mission_context)

    summary: dict[str, SignatureSummary] = {}
    for signature, data in buckets.items():
        instruments = tuple(sorted(data.instruments))
        missions = tuple(sorted(data.missions))
        summary[signature] = SignatureSummary(
            signature_type=signature,
            count=data.count,
            instruments=instruments,
            missions=missions,
        )
    return summary


def _format_collection(items: Sequence[str]) -> str:
    return ", ".join(items) if items else "—"


def format_signature_summary(summary: Mapping[str, SignatureSummary]) -> str:
    """Return a multi-line report for ``summary``."""

    if not summary:
        return "No candidates available."

    entries = sorted(
        summary.values(),
        key=lambda item: (-item.count, item.signature_type.lower()),
    )

    lines: list[str] = []
    for entry in entries:
        noun = "candidate" if entry.count == 1 else "candidates"
        lines.append(
            f"{entry.signature_type} — {entry.count} {noun}"
        )
        lines.append(f"  Instruments: {_format_collection(entry.instruments)}")
        lines.append(f"  Missions: {_format_collection(entry.missions)}")
        lines.append("")

    return "\n".join(lines).rstrip()


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Summarise the string theory observational candidate dataset."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA,
        help="Path to string_theory_observational_candidates.csv",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    candidates = load_candidates(args.data)
    summary = summarize_by_signature(candidates)
    print(format_signature_summary(summary))


if __name__ == "__main__":
    main()

