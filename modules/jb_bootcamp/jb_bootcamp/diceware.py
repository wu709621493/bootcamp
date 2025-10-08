"""Utility functions for working with Diceware-style passphrases."""

from __future__ import annotations

import math
import re
from collections.abc import Iterable, Sequence


_DEFAULT_SEPARATORS = re.compile(r"[\s._-]+")


def _coerce_to_words(passphrase: Iterable[str] | str) -> list[str]:
    """Return the words contained in ``passphrase``.

    Parameters
    ----------
    passphrase:
        Either an iterable of individual words or a string containing the
        passphrase. Strings are split on runs of whitespace, periods, dashes,
        and underscores to mimic the separators commonly used in Diceware
        phrases.

    Returns
    -------
    list[str]
        The words present in the supplied passphrase. Empty strings are
        ignored.

    """

    if isinstance(passphrase, str):
        # ``split`` never returns ``None`` and filters out empty results.
        return [word for word in _DEFAULT_SEPARATORS.split(passphrase) if word]

    if isinstance(passphrase, Sequence):
        return [word for word in passphrase if word]

    return [word for word in list(passphrase) if word]


def estimate_diceware_entropy(
    passphrase: Iterable[str] | str,
    wordlist_size: int = 7776,
) -> float:
    """Estimate the entropy, in bits, of a Diceware-style passphrase.

    The entropy of a Diceware passphrase is determined by the number of words
    chosen and the size of the source word list. This function assumes each
    word is selected independently and uniformly at random from the list.

    Parameters
    ----------
    passphrase:
        The passphrase whose strength should be estimated. The passphrase can
        be supplied either as an iterable of already-tokenized words or as a
        single string. Strings are split using the same rules as
        :func:`_coerce_to_words`.
    wordlist_size:
        The number of entries in the Diceware word list. The classic Diceware
        list has 7776 entries (six-sided dice rolled five times).

    Returns
    -------
    float
        The estimated number of bits of entropy in the passphrase.

    Raises
    ------
    ValueError
        If ``wordlist_size`` is less than 2 or if no words are detected in the
        passphrase.
    """

    if wordlist_size < 2:
        msg = "wordlist_size must be at least 2"
        raise ValueError(msg)

    words = _coerce_to_words(passphrase)
    if not words:
        msg = "passphrase must contain at least one word"
        raise ValueError(msg)

    bits_per_word = math.log2(wordlist_size)
    return len(words) * bits_per_word


__all__ = ["estimate_diceware_entropy"]

