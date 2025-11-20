import pytest

from jb_bootcamp.boss import boss_of, chain_of_command, count_reports, normalize_chart


def test_normalize_chart_rejects_cycles():
    with pytest.raises(ValueError):
        normalize_chart([("alice", "bruce"), ("bruce", "alice")])


def test_chain_and_boss():
    chart = normalize_chart(
        [
            ("alice", "bruce"),
            ("bruce", "ceo"),
            ("ceo", None),
            ("devon", "bruce"),
        ]
    )

    assert boss_of("alice", chart) == "ceo"
    assert boss_of("ceo", chart) is None
    assert chain_of_command("alice", chart) == ["alice", "bruce", "ceo"]
    assert chain_of_command("devon", chart) == ["devon", "bruce", "ceo"]


def test_count_reports_handles_indirects():
    chart = normalize_chart(
        [
            ("alice", "bruce"),
            ("bruce", "ceo"),
            ("carla", "ceo"),
            ("ceo", None),
        ]
    )
    counts = count_reports(chart)
    assert counts["alice"] == 0
    assert counts["carla"] == 0
    assert counts["bruce"] == 1
    assert counts["ceo"] == 3
