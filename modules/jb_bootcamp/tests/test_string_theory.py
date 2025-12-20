from __future__ import annotations

from pathlib import Path

from jb_bootcamp.string_theory import (
    SignatureSummary,
    InstrumentationSummary,
    Candidate,
    filter_candidates,
    format_instrumentation_summary,
    format_signature_summary,
    load_candidates,
    summarize_by_instrumentation,
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


def test_summarize_by_instrumentation_groups_signatures_and_missions() -> None:
    candidates = [
        Candidate(
            candidate="Candidate A1",
            signature_type="Signature A",
            measurement_goal="Goal A1",
            instrumentation="Scope A",
            mission_context="Mission 1",
            notes="",
        ),
        Candidate(
            candidate="Candidate A2",
            signature_type="Signature B",
            measurement_goal="Goal A2",
            instrumentation="Scope A",
            mission_context="Mission 2",
            notes="",
        ),
        Candidate(
            candidate="Candidate B",
            signature_type="Signature C",
            measurement_goal="Goal B",
            instrumentation="Scope B",
            mission_context="Mission 3",
            notes="",
        ),
    ]

    summary = summarize_by_instrumentation(candidates)

    scope_a = summary["Scope A"]
    assert scope_a.count == 2
    assert scope_a.signature_types == ("Signature A", "Signature B")
    assert scope_a.missions == ("Mission 1", "Mission 2")


def test_format_instrumentation_summary_orders_and_lists_fields() -> None:
    summary = {
        "Scope B": InstrumentationSummary(
            "Scope B",
            count=1,
            signature_types=("Signature C",),
            missions=("Mission 3",),
        ),
        "Scope A": InstrumentationSummary(
            "Scope A",
            count=2,
            signature_types=("Signature A", "Signature B"),
            missions=("Mission 1", "Mission 2"),
        ),
    }

    report = format_instrumentation_summary(summary)
    lines = [line for line in report.splitlines() if "—" in line]

    assert lines[0].startswith("Scope A — 2")
    assert "Signature A" in report
    assert "Mission 3" in report


def test_filter_candidates_applies_case_insensitive_substring_filters() -> None:
    candidates = [
        Candidate(
            candidate="Primordial gravitational wave spectrum",
            signature_type="Tensor perturbations at high multipoles",
            measurement_goal="Observe B-mode polarization",
            instrumentation="Space-based laser interferometer",
            mission_context="Next-generation LISA-like mission targeting mHz-kHz range",
            notes="",
        ),
        Candidate(
            candidate="Cosmic microwave background temperature anisotropy",
            signature_type="Scalar perturbations",
            measurement_goal="Refine spectral index",
            instrumentation="CMB surveyor",
            mission_context="Ground-based array",
            notes="",
        ),
    ]

    filtered = filter_candidates(
        candidates,
        signature_type="tensor",
        instrumentation="laser",
        mission_context="LISA",
    )

    assert [entry.candidate for entry in filtered] == [
        "Primordial gravitational wave spectrum"
    ]


def test_filter_candidates_returns_all_when_no_filters() -> None:
    candidates = [
        Candidate(
            candidate="A",
            signature_type="Type A",
            measurement_goal="Goal A",
            instrumentation="Instrument A",
            mission_context="Mission A",
            notes="",
        ),
        Candidate(
            candidate="B",
            signature_type="Type B",
            measurement_goal="Goal B",
            instrumentation="Instrument B",
            mission_context="Mission B",
            notes="",
        ),
    ]

    assert filter_candidates(candidates) == candidates

