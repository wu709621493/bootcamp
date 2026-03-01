# Translating the P vs NP Problem into Egyptian and Mayan Math

This note explains the **P vs NP** question using ideas from two ancient number systems:

- **Egyptian numerals** (additive symbols: strokes for ones, heel-bones for tens, coils for hundreds, etc.)
- **Mayan numerals** (base-20 place-value with dots, bars, and a shell for zero)

The point is not that ancient scribes studied complexity theory, but that these systems give useful metaphors.

## 1) The modern statement (brief)

- **P**: problems we can *solve* quickly (in polynomial time).
- **NP**: problems where, if someone gives us a candidate answer, we can *check* it quickly.
- **P vs NP** asks: if a solution is easy to verify, is it always easy to find?

## 2) Egyptian-math translation

Egyptian arithmetic was often procedural and table-based (especially with doubling methods).

### “Verify” in Egyptian style

Suppose someone claims:

> “These selected entries from a doubling table sum to a target total.”

Checking that claim is straightforward:

1. Recompute each doubled row.
2. Add marked rows.
3. Compare with the target.

That resembles **NP verification**: a provided witness can be checked quickly.

### “Find” in Egyptian style

Now remove the markings and ask:

> “Which combination of rows reaches the target?”

Finding the right subset can require trying many combinations. This captures the intuition behind hard search problems (like subset-sum), where finding can be much harder than checking.

So, in this metaphor:

- **NP** = “If the scribe gives you the marked rows, checking is efficient.”
- **P** = “You can also discover the marked rows efficiently yourself.”

The unresolved question is whether these are always the same power.

## 3) Mayan-math translation

Mayan numerals are compact and positional (base 20), which makes verification examples easy to picture.

### “Verify” in Mayan style

Imagine a puzzle encoded in base-20 digits (dots and bars). Someone hands you a proposed arrangement and says:

> “This arrangement satisfies all constraints.”

You can quickly test each constraint and confirm the claim. Again: easy verification with a certificate.

### “Find” in Mayan style

Without the proposed arrangement, you may need to explore a huge search space of base-20 configurations. The number of possibilities can explode as the puzzle size grows.

So the Mayan analogy says the same thing:

- Fast checking of a candidate does **not obviously** imply fast discovery of a candidate.

## 4) Unified ancient-style paraphrase

A compact “translation” of P vs NP into these systems is:

> In Egyptian tables and Mayan place-values alike, a completed answer can often be confirmed quickly; the open question is whether such answers can always be generated quickly.

That is the heart of **P vs NP**.

## 5) Important caveat

This is a pedagogical analogy, not a historical claim. P vs NP is a modern formal question in computational complexity theory.
