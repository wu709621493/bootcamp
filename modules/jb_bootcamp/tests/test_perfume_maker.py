import pytest

from jb_bootcamp.perfume_maker import (
    PerfumeNote,
    build_perfume,
    concentration_label,
    estimate_longevity_hours,
)


def test_concentration_labels() -> None:
    assert concentration_label(0.08) == "eau de cologne"
    assert concentration_label(0.15) == "eau de toilette"
    assert concentration_label(0.22) == "eau de parfum"
    assert concentration_label(0.35) == "parfum"


def test_build_perfume_outputs_note_volumes_and_accord_breakdown() -> None:
    notes = [
        PerfumeNote("bergamot", "citrus", intensity=0.6, volatility=0.9),
        PerfumeNote("rose", "floral", intensity=0.7, volatility=0.5),
        PerfumeNote("sandalwood", "woody", intensity=0.8, volatility=0.2),
    ]
    blend = build_perfume(
        notes,
        {"bergamot": 2, "rose": 3, "sandalwood": 5},
        total_volume_ml=50,
        oil_fraction=0.2,
    )

    assert blend.concentration == "eau de parfum"
    assert blend.note_volumes_ml == pytest.approx(
        {"bergamot": 2.0, "rose": 3.0, "sandalwood": 5.0}
    )
    assert blend.top_heart_base_ratio == pytest.approx((0.2, 0.3, 0.5))


def test_build_perfume_rejects_unknown_note() -> None:
    notes = [PerfumeNote("rose", "floral", intensity=0.6, volatility=0.5)]

    with pytest.raises(KeyError):
        build_perfume(notes, {"oud": 1}, total_volume_ml=30, oil_fraction=0.2)


def test_estimate_longevity_uses_note_profile() -> None:
    airy = [
        PerfumeNote("lemon", "citrus", intensity=0.4, volatility=0.95),
        PerfumeNote("neroli", "floral", intensity=0.5, volatility=0.8),
    ]
    deep = [
        PerfumeNote("labdanum", "resin", intensity=0.8, volatility=0.2),
        PerfumeNote("patchouli", "woody", intensity=0.7, volatility=0.3),
    ]

    assert estimate_longevity_hours(deep, 0.2) > estimate_longevity_hours(airy, 0.2)
