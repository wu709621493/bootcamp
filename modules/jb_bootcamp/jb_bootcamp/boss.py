"""Lightweight tools for reasoning about boss/subordinate chains.

The functions in this module help validate and traverse simple reporting
structures such as ``{"alice": "bruce", "bruce": "ceo"}``.  They are
intentionally deterministic, raise informative errors on invalid input, and do
not depend on any external libraries.
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, Iterable, Mapping, Optional, Set

__all__ = [
    "normalize_chart",
    "boss_of",
    "chain_of_command",
    "count_reports",
]


def normalize_chart(pairs: Iterable[tuple[str, Optional[str]]]) -> Dict[str, Optional[str]]:
    """Return a validated boss chart from ``pairs``.

    Each element of ``pairs`` is a two-tuple ``(employee, boss)`` where ``boss``
    may be ``None`` for a top-level leader.  The function ensures employees are
    unique, that a person is not listed as their own boss, and that the overall
    structure is acyclic.  A ``ValueError`` is raised if any rule is violated.
    """

    chart: Dict[str, Optional[str]] = {}
    for employee, boss in pairs:
        if not employee:
            raise ValueError("Employee names must be non-empty strings.")
        if employee == boss:
            raise ValueError(f"{employee!r} cannot be their own boss.")
        if employee in chart:
            raise ValueError(f"{employee!r} is already listed in the chart.")
        chart[employee] = boss

    _ensure_acyclic(chart)
    return chart


def boss_of(employee: str, chart: Mapping[str, Optional[str]]) -> Optional[str]:
    """Return the ultimate boss for ``employee``.

    The function follows each boss pointer until the top of the hierarchy is
    reached.  If ``employee`` is not present in ``chart`` a ``KeyError`` is
    raised.  ``None`` is returned when ``employee`` does not report to anyone.
    """

    if employee not in chart:
        raise KeyError(f"Unknown employee: {employee!r}")

    current = employee
    while chart[current] is not None:
        current = chart[current]  # type: ignore[assignment]
        if current not in chart:
            raise ValueError(f"Boss {current!r} is missing from the chart.")
    return None if current == employee and chart[current] is None else current


def chain_of_command(employee: str, chart: Mapping[str, Optional[str]]) -> list[str]:
    """Return the reporting chain from ``employee`` up to the top boss."""

    chain = [employee]
    current = employee
    while chart[current] is not None:
        boss = chart[current]
        if boss is None:
            break
        if boss not in chart:
            raise ValueError(f"Boss {boss!r} is missing from the chart.")
        chain.append(boss)
        current = boss
    return chain


def count_reports(chart: Mapping[str, Optional[str]]) -> Dict[str, int]:
    """Return a mapping of each boss to the total reports beneath them.

    The counts include both direct and indirect reports.  Employees who do not
    manage anyone will have a count of zero.  The function assumes ``chart`` is
    acyclic; call :func:`normalize_chart` first if in doubt.
    """

    children: Dict[str, Set[str]] = defaultdict(set)
    employees = set(chart)
    for employee, boss in chart.items():
        if boss is not None:
            children[boss].add(employee)
            employees.add(boss)

    counts = {person: 0 for person in employees}
    for person in employees:
        counts[person] = _subtree_size(person, children) - 1
    return counts


def _ensure_acyclic(chart: Mapping[str, Optional[str]]) -> None:
    """Raise ``ValueError`` if *chart* contains a reporting loop."""

    visiting: Set[str] = set()
    visited: Set[str] = set()

    def walk(employee: str) -> None:
        if employee in visited:
            return
        if employee in visiting:
            raise ValueError("A reporting cycle was detected in the chart.")

        visiting.add(employee)
        boss = chart.get(employee)
        if boss is not None:
            walk(boss)
        visiting.remove(employee)
        visited.add(employee)

    for name in chart:
        walk(name)


def _subtree_size(root: str, children: Mapping[str, Set[str]]) -> int:
    """Return the size of the subtree rooted at ``root`` (including root)."""

    size = 0
    queue: deque[str] = deque([root])
    while queue:
        current = queue.popleft()
        size += 1
        queue.extend(children.get(current, ()))
    return size
