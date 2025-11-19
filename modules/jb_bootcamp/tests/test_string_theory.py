from __future__ import annotations

from pathlib import Path

from jb_bootcamp.string_theory import (
    SignatureSummary,
    format_signature_summary,
    load_candidates,
    summarize_by_signature,
)

DATA_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "string_theory_observational_candidates.csv"
)


def test_load_candidates_parses_csv() -> None:
    candidates = load_candidates(DATA_PATH)

    assert len(candidates) >= 6
    first = candidates[0]
    assert first.candidate == "Primordial gravitational wave spectrum"
    assert first.signature_type == "Tensor perturbations at high multipoles"


def test_summarize_by_signature_collects_instruments_and_missions() -> None:
    candidates = load_candidates(DATA_PATH)
    summary = summarize_by_signature(candidates)

    tensor = summary["Tensor perturbations at high multipoles"]
    assert tensor.count == 1
    assert tensor.instruments == ("Space-based laser interferometer",)
    assert tensor.missions == ("Next-generation LISA-like mission targeting mHz-kHz range",)


def test_format_signature_summary_orders_by_count_then_name() -> None:
    summary = {
        "B": SignatureSummary("B", count=2, instruments=("Inst2",), missions=("Mission2",)),
        "A": SignatureSummary("A", count=2, instruments=("Inst1",), missions=("Mission1",)),
        "C": SignatureSummary("C", count=1, instruments=("Inst3",), missions=("Mission3",)),
    }

    report = format_signature_summary(summary)

    lines = [line for line in report.splitlines() if "—" in line]
    assert lines[0].startswith("A — 2")
    assert lines[1].startswith("B — 2")
    assert "Inst3" in report


def test_format_signature_summary_handles_empty_mapping() -> None:
    assert format_signature_summary({}) == "No candidates available."

