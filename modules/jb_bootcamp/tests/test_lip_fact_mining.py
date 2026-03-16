from jb_bootcamp.lip_fact_mining import lip_fact_mining


def test_extracts_sentences_with_lip_tokens():
    text = (
        "Lips help shape many speech sounds. "
        "Teeth are also important. "
        "Lip balm can reduce dryness in winter!"
    )

    assert lip_fact_mining(text) == [
        "Lips help shape many speech sounds.",
        "Lip balm can reduce dryness in winter!",
    ]


def test_keeps_unique_order_and_handles_empty_string():
    text = "Lip color varies. Lip color varies."
    assert lip_fact_mining(text) == ["Lip color varies."]
    assert lip_fact_mining("   ") == []
