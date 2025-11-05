# Exploring Prime Patterns

This note accompanies `prime_patterns.py`, a small exploratory module that can be
used to generalize the twin prime series and to experiment numerically with
Goldbach's conjecture.

## Generalizing the Twin Prime Series

The classical twin primes are pairs of primes separated by a gap of two.  A more
flexible way to view them is as *prime constellations* defined by a set of
offsets.  For example, the offsets `(0, 2)` describe twin primes because, given a
base prime `p`, both `p` and `p + 2` must be prime.  By supplying a different set
of offsets we can recover richer constellations:

- `(0, 2, 6)` yields prime triplets where each triple has the shape `(p, p+2, p+6)`.
- `(0, 4, 6)` captures the cousin primes `(p, p+4)` together with a bridging
  prime `p+6`.
- `(0, 2, 6, 8)` describes prime quadruplets, the densest admissible cluster of
  four primes.

The function `prime_constellation` enumerates these structures up to any chosen
limit.  It returns explicit tuples of primes, which makes it convenient to study
run-lengths, gaps, or other statistics of generalized twin-prime series.

## Goldbach's Conjecture

Goldbach's conjecture asserts that every even integer greater than 2 is the sum
of two primes.  The conjecture remains unproved, but it has been verified by
computer to extremely large bounds.  The helper `verify_goldbach` in
`prime_patterns.py` mirrors this approach in miniature: it produces one prime
partition for every even number up to a limit.  If it were to encounter an even
integer without such a partition it would raise a `GoldbachCounterexample`,
thereby falsifying the conjecture.  Of course, the absence of a counterexample in
finite computations does **not** constitute a proof—rather, it provides
supporting evidence while illustrating the numerical behavior of the conjecture.

## Running the Demonstration

From the repository root you can run a quick demo with

```bash
python -m misc.prime_patterns --limit 50000
```

The script prints summary statistics for twin primes, one family of generalized
prime constellations, and the even integers checked against Goldbach's
conjecture.
