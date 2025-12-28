"""A minimal last-in, first-out stack implementation for practice exercises."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Generic, List, TypeVar


T = TypeVar("T")


class Stack(Generic[T]):
    """Simple LIFO stack with convenience helpers."""

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._items: List[T] = list(items) if items is not None else []

    def push(self, item: T) -> None:
        """Add ``item`` to the top of the stack."""

        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top-most item.

        Raises
        ------
        IndexError
            If the stack is empty.
        """

        if not self._items:
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top-most item without removing it.

        Raises
        ------
        IndexError
            If the stack is empty.
        """

        if not self._items:
            raise IndexError("Cannot peek into an empty stack.")
        return self._items[-1]

    def clear(self) -> None:
        """Remove all items from the stack."""

        self._items.clear()

    def is_empty(self) -> bool:
        """Return ``True`` when the stack holds no items."""

        return not self._items

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._items)

    def __iter__(self) -> Iterator[T]:  # pragma: no cover - trivial
        return iter(self._items)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"{self.__class__.__name__}({self._items!r})"
