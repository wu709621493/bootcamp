"""Utility functions for exploring prime constellations and Goldbach's conjecture.

This module provides a small toolkit for enumerating generalized twin prime
sequences (also known as prime constellations) and for performing computational
checks related to Goldbach's conjecture.  The functions here are intentionally
lightweight so they can run in constrained teaching environments.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple


def sieve_of_eratosthenes(limit: int) -> List[bool]:
    """Return a boolean sieve where ``True`` indicates that the index is prime."""
    if limit < 2:
        return [False] * (limit + 1)
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for number in range(2, int(limit ** 0.5) + 1):
        if sieve[number]:
            sieve[number * number : limit + 1 : number] = [False] * (
                (limit - number * number) // number + 1
            )
    return sieve


def primes_up_to(limit: int) -> List[int]:
    """Return a list of all primes up to and including ``limit``."""
    sieve = sieve_of_eratosthenes(limit)
    return [index for index, is_prime in enumerate(sieve) if is_prime]


def prime_constellation(offsets: Sequence[int], limit: int) -> List[Tuple[int, ...]]:
    """Enumerate prime constellations defined by ``offsets``.

    ``offsets`` should be an increasing sequence of integers that starts at 0.
    The function returns tuples ``(p + o for o in offsets)`` such that every
    element of the tuple is prime and ``p + offsets[-1]`` is at most ``limit``.

    For example, ``offsets=(0, 2)`` yields the classical twin primes, while
    ``offsets=(0, 2, 6)`` yields prime triplets of the form ``(p, p+2, p+6)``.
    """
    if not offsets:
        raise ValueError("offsets must contain at least one element")
    if offsets[0] != 0:
        raise ValueError("offsets must start at 0 so that the first element is prime")

    max_offset = offsets[-1]
    sieve = sieve_of_eratosthenes(limit)
    constellations: List[Tuple[int, ...]] = []

    for base in range(2, limit - max_offset + 1):
        if all(sieve[base + offset] for offset in offsets):
            constellations.append(tuple(base + offset for offset in offsets))
    return constellations


@dataclass(frozen=True)
class GoldbachCounterexample(Exception):
    """Raised when a counterexample to Goldbach's conjecture is found."""

    even_number: int


def goldbach_partition(even_number: int, primes: Sequence[int]) -> Tuple[int, int]:
    """Return one pair of primes whose sum equals ``even_number``.

    A ``GoldbachCounterexample`` is raised if no partition is found.  This does
    not constitute a proof of the conjecture because only finitely many cases
    are checked; it merely performs a computational experiment.
    """
    primes_set = set(primes)
    for prime in primes:
        complement = even_number - prime
        if complement < 2:
            break
        if complement in primes_set:
            return prime, complement
    raise GoldbachCounterexample(even_number)


def verify_goldbach(limit: int) -> List[Tuple[int, Tuple[int, int]]]:
    """Verify Goldbach's conjecture for even numbers up to ``limit``.

    Returns a list of tuples ``(n, (p, q))`` documenting one Goldbach partition
    for each even number checked.
    """
    if limit < 4:
        return []
    if limit % 2 == 1:
        limit -= 1

    primes = primes_up_to(limit)
    partitions: List[Tuple[int, Tuple[int, int]]] = []
    for even_number in range(4, limit + 1, 2):
        partitions.append((even_number, goldbach_partition(even_number, primes)))
    return partitions


def demonstrate(limit: int = 100_000) -> None:
    """Print a short demonstration of the provided utilities."""
    twin_primes = prime_constellation((0, 2), limit)
    prime_triplets = prime_constellation((0, 2, 6), limit)

    print(f"Twin primes up to {limit}: {len(twin_primes)} examples")
    print(f"First 10 twin primes: {twin_primes[:10]}")
    print(f"Prime triplets (0, 2, 6) up to {limit}: {len(prime_triplets)} examples")
    print(f"First 10 prime triplets: {prime_triplets[:10]}")

    partitions = verify_goldbach(limit)
    print(
        f"Verified Goldbach's conjecture for even numbers up to {limit} "
        f"({len(partitions)} cases)"
    )


if __name__ == "__main__":  # pragma: no cover - manual exploration helper
    import argparse

    parser = argparse.ArgumentParser(
        description="Explore generalized twin primes and Goldbach partitions"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100_000,
        help="Upper bound for primes to consider (default: 100000)",
    )
    args = parser.parse_args()
    demonstrate(args.limit)
