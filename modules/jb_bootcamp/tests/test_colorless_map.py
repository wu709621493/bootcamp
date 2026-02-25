import pytest

from jb_bootcamp.colorless_map import colorless_map, strip_ansi


def test_strip_ansi_removes_control_sequences():
    assert strip_ansi("\x1b[31mred\x1b[0m") == "red"


def test_colorless_map_cleans_keys_and_values():
    payload = {"\x1b[32mok\x1b[0m": "\x1b[31mbad\x1b[0m"}
    assert colorless_map(payload) == {"ok": "bad"}


def test_colorless_map_can_recurse_into_nested_mappings():
    payload = {"outer": {"\x1b[34minner\x1b[0m": "\x1b[35mvalue\x1b[0m"}}
    assert colorless_map(payload, recurse=True) == {"outer": {"inner": "value"}}


def test_colorless_map_rejects_duplicate_normalized_keys():
    payload = {"\x1b[31ma\x1b[0m": 1, "a": 2}
    with pytest.raises(ValueError):
        colorless_map(payload)
