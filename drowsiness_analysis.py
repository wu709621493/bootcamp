"""Summaries of how drowsiness relates to conscious performance.

This script reads `data/gfmt_sleep.csv`, a dataset that combines the
Glasgow Face Matching Test (GFMT) with several sleep questionnaires, and
computes simple statistics showing how daytime sleepiness relates to
perceptual accuracy and confidence.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path
from typing import Dict, Iterable, List, Optional

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = REPO_ROOT / "data" / "gfmt_sleep.csv"


def _normalize_columns(columns: Iterable[str]) -> Dict[str, str]:
    return {name: name.strip().lower().replace(" ", "_") for name in columns}


def _safe_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    cleaned = value.strip()
    if cleaned in {"", "*"}:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def load_sleep_data(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        normalized = _normalize_columns(reader.fieldnames or [])
        rows: List[dict] = []
        for row in reader:
            clean_row = {}
            for key, value in row.items():
                norm_key = normalized[key]
                if norm_key == "gender":
                    clean_row[norm_key] = (value or "").strip().lower()
                else:
                    clean_row[norm_key] = _safe_float(value)
            rows.append(clean_row)
    return rows


def _mean(values: Iterable[Optional[float]]) -> float:
    filtered = [v for v in values if v is not None]
    return statistics.fmean(filtered) if filtered else float("nan")


def _pearson(x_values: Iterable[Optional[float]], y_values: Iterable[Optional[float]]) -> float:
    pairs = [
        (x, y)
        for x, y in zip(x_values, y_values)
        if x is not None and y is not None
    ]
    if len(pairs) < 2:
        return float("nan")

    xs, ys = zip(*pairs)
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    denominator = math.sqrt(
        sum((x - mean_x) ** 2 for x in xs) * sum((y - mean_y) ** 2 for y in ys)
    )
    return numerator / denominator if denominator else float("nan")


def summarize_drowsiness(rows: List[dict]) -> Dict[str, float]:
    ess = [row.get("ess") for row in rows]
    percent_correct = [row.get("percent_correct") for row in rows]
    conf_correct = [row.get("confidence_when_correct") for row in rows]
    conf_reject = [row.get("confidence_when_correct_reject") for row in rows]

    high_mask = [val is not None and val >= 10 for val in ess]
    low_mask = [val is not None and val < 10 for val in ess]

    def _group_mean(values: List[Optional[float]], mask: List[bool]) -> float:
        grouped = [val for val, keep in zip(values, mask) if keep and val is not None]
        return statistics.fmean(grouped) if grouped else float("nan")

    summary = {
        "n_participants": len(rows),
        "mean_ess": _mean(ess),
        "median_ess": statistics.median([val for val in ess if val is not None])
        if any(val is not None for val in ess)
        else float("nan"),
        "corr_ess_percent": _pearson(ess, percent_correct),
        "corr_ess_confidence": _pearson(ess, conf_correct),
        "low_drowsy_mean_percent": _group_mean(percent_correct, low_mask),
        "high_drowsy_mean_percent": _group_mean(percent_correct, high_mask),
        "low_drowsy_confidence": _group_mean(conf_correct, low_mask),
        "high_drowsy_confidence": _group_mean(conf_correct, high_mask),
    }

    summary.update(
        {
            "corr_ess_reject_confidence": _pearson(ess, conf_reject),
            "low_drowsy_reject_confidence": _group_mean(conf_reject, low_mask),
            "high_drowsy_reject_confidence": _group_mean(conf_reject, high_mask),
        }
    )

    return summary


def format_summary(summary: Dict[str, float]) -> str:
    lines = [
        f"Participants analyzed: {summary['n_participants']}",
        f"Mean ESS (sleepiness score): {summary['mean_ess']:.2f}",
        f"Median ESS: {summary['median_ess']:.2f}",
        "",
        "Relationships with accuracy/confidence:",
        f"  Corr(ESS, percent correct): {summary['corr_ess_percent']:.3f}",
        f"  Corr(ESS, confidence when correct): {summary['corr_ess_confidence']:.3f}",
        f"  Corr(ESS, confidence when correct reject): "
        f"{summary['corr_ess_reject_confidence']:.3f}",
        "",
        "Group means (ESS < 10 = low drowsiness):",
        "  Percent correct:",
        f"    Low drowsiness:  {summary['low_drowsy_mean_percent']:.2f}",
        f"    High drowsiness: {summary['high_drowsy_mean_percent']:.2f}",
        "  Confidence when correct:",
        f"    Low drowsiness:  {summary['low_drowsy_confidence']:.2f}",
        f"    High drowsiness: {summary['high_drowsy_confidence']:.2f}",
        "  Confidence when correct reject:",
        f"    Low drowsiness:  {summary['low_drowsy_reject_confidence']:.2f}",
        f"    High drowsiness: {summary['high_drowsy_reject_confidence']:.2f}",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Summarize how drowsiness (ESS) relates to accuracy and confidence "
            "using the GFMT sleep dataset."
        )
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA,
        help="Path to gfmt_sleep.csv (defaults to the repository data file).",
    )
    args = parser.parse_args()

    rows = load_sleep_data(args.data)
    summary = summarize_drowsiness(rows)
    print(format_summary(summary))


if __name__ == "__main__":
    main()

