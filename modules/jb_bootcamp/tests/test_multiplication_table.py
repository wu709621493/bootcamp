"""Tests for the Chinese multiplication table helpers."""

from __future__ import annotations

import pytest

from jb_bootcamp.multiplication_table import (
    build_table,
    format_table,
    product_line,
    table_as_text,
    to_chinese_digit,
    to_chinese_number,
)


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "一"),
        (5, "五"),
        (9, "九"),
    ],
)
def test_to_chinese_digit(value: int, expected: str) -> None:
    assert to_chinese_digit(value) == expected


def test_to_chinese_digit_rejects_out_of_range() -> None:
    with pytest.raises(ValueError):
        to_chinese_digit(0)


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "一"),
        (9, "九"),
        (10, "十"),
        (11, "十一"),
        (20, "二十"),
        (21, "二十一"),
        (32, "三十二"),
    ],
)
def test_to_chinese_number(value: int, expected: str) -> None:
    assert to_chinese_number(value) == expected


def test_to_chinese_number_rejects_out_of_range() -> None:
    with pytest.raises(ValueError):
        to_chinese_number(0)


@pytest.mark.parametrize(
    "multiplicand, multiplier, expected",
    [
        (1, 1, "一一得一"),
        (1, 2, "一二得二"),
        (3, 7, "三七得二十一"),
        (9, 9, "九九得八十一"),
    ],
)
def test_product_line(multiplicand: int, multiplier: int, expected: str) -> None:
    assert product_line(multiplicand, multiplier) == expected


def test_build_table_rows() -> None:
    assert build_table(2) == [["一一得一", "一二得二"], ["二二得四"]]


def test_format_table() -> None:
    rows = [["一一得一", "一二得二"], ["二二得四"]]
    assert format_table(rows) == "一一得一  一二得二\n二二得四"


def test_table_as_text_default() -> None:
    table = table_as_text(3)
    assert "一一得一" in table
    assert "二三得六" in table
    assert "三三得九" in table


def test_build_table_rejects_invalid_max_factor() -> None:
    with pytest.raises(ValueError):
        build_table(0)


def test_product_line_rejects_invalid_factor() -> None:
    with pytest.raises(ValueError):
        product_line(0, 1)
