"""Helpers for balancing Cantonese tone practice lists.

The functions here normalize Jyutping strings, compute tone distributions, and
rank phrases that help cover underrepresented tones.  They are intentionally
lightweight so they can be used in notebooks or small curriculum-planning
scripts without additional dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence
import re

__all__ = [
    "CantonesePhrase",
    "split_jyutping",
    "tone_distribution",
    "analyze_phrasebook",
    "prioritize_phrases",
]


_JYUTPING_RE = re.compile(r"[a-z]{1,6}\d", re.IGNORECASE)


@dataclass(frozen=True)
class CantonesePhrase:
    """Container for a Cantonese phrase and its Jyutping romanization."""

    hanzi: str
    jyutping: str
    gloss: str | None = None

    def syllables(self) -> tuple[str, ...]:
        """Return normalized Jyutping syllables with tone digits."""

        return split_jyutping(self.jyutping)

    def tones(self) -> tuple[int, ...]:
        """Return the tone numbers for each syllable in the phrase."""

        return tuple(_tone_from_syllable(syllable) for syllable in self.syllables())


def split_jyutping(text: str) -> tuple[str, ...]:
    """Split and normalize a Jyutping string into syllables.

    Accepts space, hyphen, comma, or slash as separators and enforces that each
    token ends with a tone digit in ``1``–``6``.  Tokens are lowercased and
    surrounding punctuation is ignored.
    """

    tokens = re.split(r"[\s,/\\-]+", text.strip())
    syllables: list[str] = []

    for token in tokens:
        if not token:
            continue
        cleaned = re.sub(r"[^A-Za-z0-9]", "", token).lower()
        if not _JYUTPING_RE.fullmatch(cleaned):
            raise ValueError(f"Invalid Jyutping token: {token!r}")
        syllables.append(cleaned)

    return tuple(syllables)


def tone_distribution(syllables: Sequence[str]) -> dict[int, int]:
    """Count tone occurrences in a sequence of Jyutping syllables."""

    counts: dict[int, int] = {tone: 0 for tone in range(1, 7)}
    for syllable in syllables:
        tone = _tone_from_syllable(syllable)
        counts[tone] += 1
    return counts


def analyze_phrasebook(
    phrases: Sequence[CantonesePhrase],
    *,
    target_mix: Mapping[int, float] | None = None,
) -> dict[str, object]:
    """Summarize tone coverage for the provided phrases."""

    all_syllables = [syllable for phrase in phrases for syllable in phrase.syllables()]
    dist = tone_distribution(all_syllables)

    total = sum(dist.values())
    if total == 0:
        balance = 1.0
    else:
        target = target_mix or {tone: 1 / 6 for tone in range(1, 7)}
        norm = {tone: max(weight, 0.0) for tone, weight in target.items() if 1 <= tone <= 6}
        if not norm:
            norm = {tone: 1 / 6 for tone in range(1, 7)}
        norm_total = sum(norm.values()) or 1.0
        normalized_target = {tone: weight / norm_total for tone, weight in norm.items()}

        balance = 0.0
        for tone, count in dist.items():
            observed = count / total if total else 0.0
            expected = normalized_target.get(tone, 0.0)
            balance += 1.0 - abs(observed - expected)
        balance = round(balance / 6, 3)

    return {
        "phrase_count": len(phrases),
        "syllable_count": total,
        "tone_distribution": dist,
        "balance_score": balance,
    }


def prioritize_phrases(
    phrases: Iterable[CantonesePhrase],
    *,
    target_mix: Mapping[int, float] | None = None,
) -> list[CantonesePhrase]:
    """Order phrases to emphasize underrepresented tones."""

    target = target_mix or {tone: 1.0 for tone in range(1, 7)}
    weights = {tone: max(weight, 0.0) for tone, weight in target.items() if 1 <= tone <= 6}
    weights = weights or {tone: 1.0 for tone in range(1, 7)}

    def rarity_score(phrase: CantonesePhrase) -> float:
        if not phrase.syllables():
            return 0.0
        scores = [1.0 / (weights.get(_tone_from_syllable(syllable), 1.0) or 1.0) for syllable in phrase.syllables()]
        return max(scores)

    return sorted(phrases, key=lambda phrase: (-rarity_score(phrase), phrase.hanzi))


def _tone_from_syllable(syllable: str) -> int:
    if not syllable or not syllable[-1].isdigit():
        raise ValueError(f"Syllable must end with a tone digit: {syllable!r}")
    tone = int(syllable[-1])
    if tone not in {1, 2, 3, 4, 5, 6}:
        raise ValueError(f"Tone must be 1-6: {syllable!r}")
    return tone

