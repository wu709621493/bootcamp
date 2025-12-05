from jb_bootcamp.project_cantonese import (
    CantonesePhrase,
    analyze_phrasebook,
    prioritize_phrases,
    split_jyutping,
    tone_distribution,
)


def test_split_and_distribution():
    syllables = split_jyutping("Nei5 hou2/ma3?")
    assert syllables == ("nei5", "hou2", "ma3")

    counts = tone_distribution(syllables)
    assert counts[5] == 1
    assert counts[2] == 1
    assert counts[3] == 1


def test_phrasebook_summary():
    phrases = [
        CantonesePhrase("你好", "nei5 hou2", gloss="hello"),
        CantonesePhrase("飲茶", "jam2 caa4", gloss="drink tea"),
    ]

    summary = analyze_phrasebook(phrases)
    assert summary["phrase_count"] == 2
    assert summary["syllable_count"] == 4
    assert summary["tone_distribution"][4] == 1
    assert 0.0 <= summary["balance_score"] <= 1.0


def test_prioritize_underrepresented_tones():
    phrases = [
        CantonesePhrase("細佬", "sai3 lou2"),
        CantonesePhrase("士多啤梨", "si6 do1 be1 lei2"),
        CantonesePhrase("粵語", "jyut6 jyu5"),
    ]

    target_mix = {1: 0.5, 6: 0.5}
    ordered = prioritize_phrases(phrases, target_mix=target_mix)

    # The phrase with tone 6 should surface first because of the weighting.
    assert ordered[0].hanzi == "士多啤梨"

