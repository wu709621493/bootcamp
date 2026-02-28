"""Tests for HIV cocktail rebuilding helpers."""

from jb_bootcamp.hiv_cocktail import rebuild_hiv_cocktail


def test_rebuild_prefers_supported_anchor_classes() -> None:
    cocktail = rebuild_hiv_cocktail(["Tenofovir Alafenamide", "Emtricitabine", "Doravirine"])

    assert cocktail.backbone == ("tenofovir alafenamide", "emtricitabine")
    assert cocktail.anchor == "doravirine"
    assert cocktail.extras == ()
    assert cocktail.unknown == ()


def test_rebuild_filters_discouraged_pi_agents() -> None:
    cocktail = rebuild_hiv_cocktail(["tenofovir alafenamide", "emtricitabine", "lopinavir"])

    assert cocktail.backbone == ("tenofovir alafenamide", "emtricitabine")
    assert cocktail.anchor is None
    assert cocktail.extras == ()
    assert "Discouraged PI agents were filtered out: lopinavir." in cocktail.notes
