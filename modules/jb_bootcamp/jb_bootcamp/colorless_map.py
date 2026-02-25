"""Helpers for removing ANSI colour codes from mapping data.

The module exposes :func:`colorless_map`, a small utility that strips ANSI
terminal escape sequences from mapping keys and/or values while preserving the
input order.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

__all__ = ["colorless_map", "strip_ansi"]

# Matches CSI-based ANSI escapes (for colours and other terminal styling).
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def strip_ansi(text: str) -> str:
    """Return *text* with ANSI terminal escape sequences removed."""

    return _ANSI_ESCAPE_RE.sub("", text)


def _strip_value(value: Any, *, recurse: bool) -> Any:
    if isinstance(value, str):
        return strip_ansi(value)
    if recurse and isinstance(value, Mapping):
        return colorless_map(value, recurse=True)
    return value


def colorless_map(
    mapping: Mapping[Any, Any],
    *,
    strip_keys: bool = True,
    strip_values: bool = True,
    recurse: bool = False,
) -> dict[Any, Any]:
    """Return a plain ``dict`` with ANSI escape sequences removed.

    Parameters
    ----------
    mapping:
        Source mapping to clean.
    strip_keys, strip_values:
        Control whether string keys and/or string values are cleaned.
    recurse:
        If ``True``, nested mappings found as values are also cleaned.

    Raises
    ------
    TypeError
        If *mapping* is not a mapping object.
    ValueError
        If key normalisation causes duplicate keys.
    """

    if not isinstance(mapping, Mapping):
        raise TypeError("mapping must be a mapping.")

    cleaned: dict[Any, Any] = {}
    source_keys: dict[Any, Any] = {}
    for key, value in mapping.items():
        new_key = strip_ansi(key) if strip_keys and isinstance(key, str) else key
        new_value = _strip_value(value, recurse=recurse) if strip_values else value

        if new_key in cleaned and source_keys[new_key] != key:
            raise ValueError("ANSI stripping produced duplicate keys.")

        cleaned[new_key] = new_value
        source_keys[new_key] = key

    return cleaned
