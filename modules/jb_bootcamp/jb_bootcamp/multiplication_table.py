"""Utilities for generating the classic Chinese nine-nine multiplication table."""

from __future__ import annotations

import argparse
from typing import Iterable, Sequence

__all__ = [
    "to_chinese_digit",
    "to_chinese_number",
    "product_line",
    "build_table",
    "format_table",
    "table_as_text",
]


_DIGITS = {
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
}


def to_chinese_digit(value: int) -> str:
    """Return the Chinese numeral for a single digit between 1 and 9."""

    try:
        return _DIGITS[value]
    except KeyError as error:
        raise ValueError("Only digits in the range 1-9 are supported") from error


def to_chinese_number(value: int) -> str:
    """Return the Chinese numeral for ``value`` (1 ≤ value ≤ 99)."""

    if not 1 <= value <= 99:
        raise ValueError("Only values between 1 and 99 can be rendered")

    if value < 10:
        return to_chinese_digit(value)

    tens, ones = divmod(value, 10)
    parts = []
    if tens == 1:
        parts.append("十")
    else:
        parts.append(f"{to_chinese_digit(tens)}十")
    if ones:
        parts.append(to_chinese_digit(ones))
    return "".join(parts)


def product_line(multiplicand: int, multiplier: int) -> str:
    """Return a recitation line, e.g. ``一二得二`` for 1×2."""

    if not (1 <= multiplicand <= 9 and 1 <= multiplier <= 9):
        raise ValueError("Multiplication table factors must be between 1 and 9")

    left = to_chinese_digit(multiplicand)
    right = to_chinese_digit(multiplier)
    product = to_chinese_number(multiplicand * multiplier)
    return f"{left}{right}得{product}"


def build_table(max_factor: int = 9) -> list[list[str]]:
    """Return rows of the traditional triangular multiplication table."""

    if not 1 <= max_factor <= 9:
        raise ValueError("max_factor must be between 1 and 9")

    rows: list[list[str]] = []
    for left in range(1, max_factor + 1):
        row = [product_line(left, right) for right in range(left, max_factor + 1)]
        rows.append(row)
    return rows


def format_table(rows: Iterable[Sequence[str]]) -> str:
    """Format ``rows`` as a multi-line string for recitation."""

    formatted_rows = ["  ".join(row) for row in rows]
    return "\n".join(formatted_rows)


def table_as_text(max_factor: int = 9) -> str:
    """Convenience helper that formats the table for ``max_factor``."""

    return format_table(build_table(max_factor))


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Recite the classic Chinese nine-nine multiplication table."
    )
    parser.add_argument(
        "--max-factor",
        type=int,
        default=9,
        help="Largest factor to include (1-9, default: 9)",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    print(table_as_text(args.max_factor))


if __name__ == "__main__":  # pragma: no cover - exercised via CLI
    main()
