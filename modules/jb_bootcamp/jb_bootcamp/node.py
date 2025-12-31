"""Singly linked list node utilities.

The :class:`Node` class is intentionally lightweight but comes with a few
helpers that make it pleasant to work with in teaching exercises.  It is
a generic container that stores a value and a reference to the next node
in the sequence.  Nodes can be chained together manually, or built from
an iterable using :meth:`Node.from_iterable`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, Optional, TypeVar

__all__ = ["Node"]

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    """A node in a singly linked list.

    Parameters
    ----------
    value:
        The data payload to store in the node.
    next:
        The next node in the chain or ``None`` to mark the end of the list.
    """

    value: T
    next: Optional["Node[T]"] = None

    def append(self, value: T) -> "Node[T]":
        """Append ``value`` after the current tail and return the new node.

        The traversal starts at the current node, walks to the end of the
        chain, and attaches a freshly created node containing ``value``.
        The method returns the appended node so callers can keep a handle
        to the new tail if desired.
        """

        current = self
        while current.next is not None:
            current = current.next
        current.next = Node(value)
        return current.next

    def __iter__(self) -> Iterator[T]:
        """Iterate over node values from this node onward."""

        current: Optional["Node[T]"] = self
        while current is not None:
            yield current.value
            current = current.next

    def __len__(self) -> int:
        """Return the number of nodes in the chain starting here."""

        count = 0
        current: Optional["Node[T]"] = self
        while current is not None:
            count += 1
            current = current.next
        return count

    def to_list(self) -> list[T]:
        """Return a ``list`` of values starting from this node."""

        return list(iter(self))

    def find(self, value: T) -> Optional["Node[T]"]:
        """Return the first node whose value matches ``value``.

        If no such node exists in the chain beginning at ``self``, the
        method returns ``None``.
        """

        current: Optional["Node[T]"] = self
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    @classmethod
    def from_iterable(cls, values: Iterable[T]) -> "Node[T]":
        """Construct a linked list from ``values`` and return its head.

        Raises
        ------
        ValueError
            If ``values`` is empty.
        """

        iterator = iter(values)
        try:
            first_value = next(iterator)
        except StopIteration as exc:
            raise ValueError("cannot build a Node chain from an empty iterable") from exc

        head = cls(first_value)
        tail = head
        for value in iterator:
            tail = tail.append(value)
        return head
