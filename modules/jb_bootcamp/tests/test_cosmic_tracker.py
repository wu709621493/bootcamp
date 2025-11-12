from __future__ import annotations

import pytest

from jb_bootcamp.cosmic_tracker import (
    CosmicCandidate,
    filter_candidates,
    load_candidates,
    summarize_by_instrumentation,
)


@pytest.fixture(scope="module")
def dataset() -> tuple[CosmicCandidate, ...]:
    return load_candidates()


def test_load_candidates_structure(dataset: tuple[CosmicCandidate, ...]) -> None:
    assert len(dataset) == 8
    first = dataset[0]
    assert first.candidate == "Primordial gravitational wave spectrum"
    assert first.instrumentation == "Space-based laser interferometer"


def test_filter_candidates_keyword(dataset: tuple[CosmicCandidate, ...]) -> None:
    filtered = filter_candidates(dataset, keyword="cosmic")
    names = {candidate.candidate for candidate in filtered}
    assert "High-energy cosmic ray cutoff anomalies" in names
    assert "Cosmic superstring lensing events" in names
    assert all("cosmic" in " ".join(vars(candidate).values()).lower() for candidate in filtered)


def test_filter_by_signature_and_instrument(dataset: tuple[CosmicCandidate, ...]) -> None:
    filtered = filter_candidates(
        dataset,
        signature_type="Microlensing caustic crossings",
        instrumentation="Wide-field infrared survey telescope",
    )
    assert [candidate.candidate for candidate in filtered] == [
        "Cosmic superstring lensing events"
    ]


def test_summarize_by_instrumentation(dataset: tuple[CosmicCandidate, ...]) -> None:
    summary = summarize_by_instrumentation(dataset)
    calorimeter = summary["Large-area cosmic ray calorimeter"]
    assert [candidate.candidate for candidate in calorimeter] == [
        "High-energy cosmic ray cutoff anomalies"
    ]
    assert summary["Wide-field near-infrared imager"][0].mission_context.startswith(
        "Distributed swarm"
    )
