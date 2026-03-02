"""Thread-safe bank account helper for bootcamp exercises."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock


@dataclass
class BankAccount:
    """A minimal bank account with explicit open/close semantics.

    The implementation is intentionally small but safe for concurrent balance
    updates in teaching examples that use multiple threads.
    """

    _is_open: bool = field(default=False, init=False)
    _balance: int = field(default=0, init=False)
    _lock: Lock = field(default_factory=Lock, init=False, repr=False)

    def open(self) -> None:
        """Open the account and reset its balance to zero."""
        with self._lock:
            if self._is_open:
                raise ValueError("account already open")
            self._is_open = True
            self._balance = 0

    def close(self) -> None:
        """Close the account.

        Closed accounts cannot be queried or modified.
        """
        with self._lock:
            if not self._is_open:
                raise ValueError("account not open")
            self._is_open = False

    def get_balance(self) -> int:
        """Return the current account balance."""
        with self._lock:
            self._ensure_open()
            return self._balance

    def increment_balance(self, amount: int) -> None:
        """Increment the balance by ``amount``.

        ``amount`` may be positive (deposit) or negative (withdrawal).
        """
        with self._lock:
            self._ensure_open()
            if not isinstance(amount, int):
                raise TypeError("amount must be an integer")
            self._balance += amount

    def _ensure_open(self) -> None:
        if not self._is_open:
            raise ValueError("account not open")
