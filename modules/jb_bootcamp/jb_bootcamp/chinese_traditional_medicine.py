"""Utilities for decoding Chinese Traditional Medicine pattern codes.

This module contains a small knowledge base with common Chinese
Traditional Medicine (TCM) diagnostic patterns.  Patterns are stored in a
structured :class:`TCMPattern` data class and can be retrieved with helper
functions that normalise a variety of textual representations.  The goal is
to provide a lightweight decoder that can translate terse pattern mnemonics
such as ``"Sp Qi Def"`` or ``"gan-qi-yu"`` into rich, human readable
descriptions including hallmark symptoms and treatment principles.

The decoder intentionally focuses on being forgiving with its input.  Many
patterns are referenced in clinical notes using different separators,
capitalisation, or even Chinese pinyin fragments.  The ``decode_pattern``
function therefore performs aggressive normalisation and tries multiple
fall-back strategies (including token permutations) before giving up.  This
behaviour makes the function resilient when working with archival records or
OCR output where consistency is not guaranteed.
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import re
from typing import Dict, Iterable, Iterator, List, Mapping, Sequence, Tuple

__all__ = [
    "TCMPattern",
    "UnknownPatternError",
    "available_patterns",
    "decode_pattern",
    "decode_sequence",
    "explain_pattern",
    "search_patterns",
]


class UnknownPatternError(KeyError):
    """Raised when a requested TCM pattern code cannot be decoded."""


@dataclass(frozen=True)
class TCMPattern:
    """Representation of a Traditional Chinese Medicine diagnostic pattern.

    Parameters
    ----------
    code:
        Canonical short code used as the key in the module's knowledge base.
    name:
        Full human readable name of the diagnostic pattern.
    organ:
        Primary zang-fu organ associated with the pattern.  Systemic or
        channel level pathologies use descriptive labels such as "Systemic".
    element:
        Five phase element (e.g. Earth, Water) most strongly associated with
        the pattern.  While simplified, the information provides helpful
        context when teaching students about inter-element relationships.
    description:
        Short summary describing the pathology.
    key_symptoms:
        Tuple containing hallmark symptoms or clinical findings.
    treatment_principle:
        Concise statement outlining the main therapeutic strategy.
    """

    code: str
    name: str
    organ: str
    element: str
    description: str
    key_symptoms: Tuple[str, ...]
    treatment_principle: str

    def matches_keyword(self, keyword: str) -> bool:
        """Return ``True`` if *keyword* appears in any textual field.

        The comparison is case-insensitive and searches the code, name,
        organ, element, description, treatment principle, and symptoms.
        """

        if not keyword:
            return False
        lowered = keyword.casefold()
        haystacks: Iterable[str] = (
            self.code,
            self.name,
            self.organ,
            self.element,
            self.description,
            self.treatment_principle,
        )
        if any(lowered in field.casefold() for field in haystacks):
            return True
        return any(lowered in symptom.casefold() for symptom in self.key_symptoms)


# Canonical token aliases used during code normalisation.  The mapping is
# intentionally expansive so that a wide range of transliterations and
# abbreviations can be decoded reliably.
_TOKEN_ALIASES: Mapping[str, str] = {
    # Organs and channels
    "SPLEEN": "SP",
    "SPL": "SP",
    "SP": "SP",
    "PI": "SP",
    "KIDNEY": "KD",
    "KID": "KD",
    "KD": "KD",
    "SHEN": "KD",
    "LIVER": "LV",
    "LIV": "LV",
    "LV": "LV",
    "GAN": "LV",
    "HEART": "HT",
    "HT": "HT",
    "XIN": "HT",
    "LUNG": "LU",
    "LU": "LU",
    "FEI": "LU",
    "STOMACH": "ST",
    "ST": "ST",
    "WEI": "ST",
    "GALLBLADDER": "GB",
    "GB": "GB",
    "DAN": "GB",
    "BLADDER": "BL",
    "URINARY": "BL",
    "BL": "BL",
    "PANGGUANG": "BL",
    # Energetic substances
    "BLOOD": "BLOOD",
    "XUE": "BLOOD",
    "QI": "QI",
    "CHI": "QI",
    "ESSENCE": "JING",
    "JING": "JING",
    "FLUID": "FLUIDS",
    "FLUIDS": "FLUIDS",
    # Yin-Yang, qualities, and states
    "YIN": "YIN",
    "YANG": "YANG",
    "DEFICIENCY": "DEF",
    "DEFIC": "DEF",
    "DEF": "DEF",
    "XU": "DEF",
    "VACUITY": "DEF",
    "INSUFFICIENCY": "DEF",
    "INSUFF": "DEF",
    "DEPLETION": "DEF",
    "STAGNATION": "STAG",
    "STAGN": "STAG",
    "STAG": "STAG",
    "YU": "STAG",
    "DEPRESSED": "STAG",
    "CONGESTION": "STAG",
    "OBSTRUCTION": "STAG",
    "STASIS": "STASIS",
    "YUAN": "STASIS",
    "JI": "STASIS",
    "BIND": "STASIS",
    "DAMP": "DAMP",
    "DAMPNESS": "DAMP",
    "SHI": "DAMP",
    "PHLEGM": "PHLEGM",
    "TAN": "PHLEGM",
    "HEAT": "HEAT",
    "RE": "HEAT",
    "FIRE": "FIRE",
    "HOT": "HEAT",
    "WARM": "HEAT",
    "COLD": "COLD",
    "HAN": "COLD",
    "WIND": "WIND",
    "FENG": "WIND",
    "DRYNESS": "DRY",
    "DRY": "DRY",
    "ARIDITY": "DRY",
    "INSUFF_YIN": "YIN_DEF",
}


_PATTERN_DATA: Dict[str, TCMPattern] = {
    "SP_QI_DEF": TCMPattern(
        code="SP_QI_DEF",
        name="Spleen Qi Deficiency",
        organ="Spleen",
        element="Earth",
        description=(
            "The spleen fails to properly transform and transport food, leading "
            "to fatigue and damp accumulation."
        ),
        key_symptoms=(
            "poor appetite",
            "loose stools",
            "fatigue",
            "abdominal distention after eating",
            "pale tongue with teeth marks",
        ),
        treatment_principle="Tonify Spleen Qi and support digestion.",
    ),
    "QI_DEF": TCMPattern(
        code="QI_DEF",
        name="Qi Deficiency",
        organ="Systemic",
        element="Earth",
        description="General lack of qi leading to diminished vitality and function.",
        key_symptoms=(
            "fatigue",
            "spontaneous sweating",
            "weak voice",
            "shortness of breath",
        ),
        treatment_principle="Tonify qi and strengthen the body's upright energy.",
    ),
    "KD_YANG_DEF": TCMPattern(
        code="KD_YANG_DEF",
        name="Kidney Yang Deficiency",
        organ="Kidney",
        element="Water",
        description=(
            "Decline of minister fire leading to coldness, edema, and impaired "
            "warming of the lower burner."
        ),
        key_symptoms=(
            "cold limbs",
            "soreness of the lower back",
            "abundant clear urination",
            "edema",
        ),
        treatment_principle="Warm and tonify Kidney yang.",
    ),
    "KD_YIN_DEF": TCMPattern(
        code="KD_YIN_DEF",
        name="Kidney Yin Deficiency",
        organ="Kidney",
        element="Water",
        description=(
            "Insufficient Kidney yin fails to nourish the essence leading to "
            "deficiency heat signs."
        ),
        key_symptoms=(
            "night sweats",
            "tinnitus",
            "five palm heat",
            "low back soreness",
        ),
        treatment_principle="Nourish Kidney yin and anchor yang.",
    ),
    "LV_QI_STAG": TCMPattern(
        code="LV_QI_STAG",
        name="Liver Qi Stagnation",
        organ="Liver",
        element="Wood",
        description="Constraint of liver qi impeding smooth flow of emotions and qi.",
        key_symptoms=(
            "distending hypochondriac pain",
            "frequent sighing",
            "emotional frustration",
            "irregular menstruation",
        ),
        treatment_principle="Soothe Liver qi and relieve stagnation.",
    ),
    "LV_BLOOD_DEF": TCMPattern(
        code="LV_BLOOD_DEF",
        name="Liver Blood Deficiency",
        organ="Liver",
        element="Wood",
        description="Insufficient Liver blood fails to nourish tendons and eyes.",
        key_symptoms=(
            "blurred vision",
            "dry eyes",
            "brittle nails",
            "scanty menses",
        ),
        treatment_principle="Nourish Liver blood and tonify yin.",
    ),
    "HT_YIN_DEF": TCMPattern(
        code="HT_YIN_DEF",
        name="Heart Yin Deficiency",
        organ="Heart",
        element="Fire",
        description="Deficient Heart yin fails to cool the spirit, causing restlessness.",
        key_symptoms=(
            "palpitations",
            "insomnia",
            "night sweats",
            "dry mouth",
        ),
        treatment_principle="Nourish Heart yin and calm the spirit.",
    ),
    "LU_QI_DEF": TCMPattern(
        code="LU_QI_DEF",
        name="Lung Qi Deficiency",
        organ="Lung",
        element="Metal",
        description="Weak Lung qi impairs respiration and defensive qi.",
        key_symptoms=(
            "shortness of breath",
            "weak cough",
            "spontaneous sweating",
            "susceptibility to colds",
        ),
        treatment_principle="Tonify Lung qi and consolidate the exterior.",
    ),
    "ST_HEAT": TCMPattern(
        code="ST_HEAT",
        name="Stomach Heat",
        organ="Stomach",
        element="Earth",
        description="Excess heat in the stomach leading to rapid digestion and thirst.",
        key_symptoms=(
            "burning epigastric pain",
            "voracious appetite",
            "excessive thirst",
            "bad breath",
        ),
        treatment_principle="Clear Stomach heat and descend rebellion.",
    ),
    "GB_DAMP_HEAT": TCMPattern(
        code="GB_DAMP_HEAT",
        name="Gallbladder Damp-Heat",
        organ="Gallbladder",
        element="Wood",
        description="Damp-heat obstructs the Gallbladder channel causing bitter taste and nausea.",
        key_symptoms=(
            "bitter taste in the mouth",
            "nausea",
            "yellow greasy tongue coating",
            "hypochondriac fullness",
        ),
        treatment_principle="Clear damp-heat from the Liver and Gallbladder.",
    ),
    "BLOOD_STASIS": TCMPattern(
        code="BLOOD_STASIS",
        name="Blood Stasis",
        organ="Systemic",
        element="Fire",
        description="Congealed blood obstructs the channels leading to sharp fixed pain.",
        key_symptoms=(
            "sharp fixed pain",
            "purple tongue",
            "choppy pulse",
            "dark clots",
        ),
        treatment_principle="Invigorate blood and dispel stasis.",
    ),
    "PHLEGM_DAMP": TCMPattern(
        code="PHLEGM_DAMP",
        name="Phlegm-Damp Accumulation",
        organ="Spleen",
        element="Earth",
        description=(
            "Accumulation of phlegm and dampness obstructs qi flow and yang "
            "transformation."
        ),
        key_symptoms=(
            "oppressive chest sensation",
            "profuse sputum",
            "obesity",
            "slippery pulse",
        ),
        treatment_principle="Transform phlegm, drain dampness, and strengthen the Spleen.",
    ),
    "WIND_COLD": TCMPattern(
        code="WIND_COLD",
        name="Wind-Cold Invasion",
        organ="Lung",
        element="Metal",
        description="External wind-cold obstructs the Lung defensive qi.",
        key_symptoms=(
            "aversion to cold",
            "fever without sweating",
            "occipital stiffness",
            "floating tight pulse",
        ),
        treatment_principle="Release the exterior and disperse wind-cold.",
    ),
    "WIND_HEAT": TCMPattern(
        code="WIND_HEAT",
        name="Wind-Heat Invasion",
        organ="Lung",
        element="Metal",
        description="Exterior wind-heat invades the Lung and impairs the wei qi.",
        key_symptoms=(
            "fever",
            "sore throat",
            "thirst",
            "floating rapid pulse",
        ),
        treatment_principle="Release the exterior and clear heat.",
    ),
}


def _normalise_tokens(code: str) -> List[str]:
    """Return a list of canonical tokens for *code*.

    The function removes punctuation, splits on underscores or whitespace and
    applies the :data:`_TOKEN_ALIASES` mapping.  Empty tokens are discarded.
    """

    cleaned = re.sub(r"[^0-9A-Za-z]+", "_", code).upper().strip("_")
    if not cleaned:
        return []
    tokens = [token for token in cleaned.split("_") if token]
    canonical_tokens = [_TOKEN_ALIASES.get(token, token) for token in tokens]
    return canonical_tokens


def _candidate_codes(tokens: Sequence[str]) -> Iterator[str]:
    """Yield potential canonical codes derived from *tokens*."""

    if not tokens:
        return iter(())
    # Direct join of tokens.
    joined = "_".join(tokens)
    yield joined

    # Try permutations for up to five tokens to keep the search tractable.
    max_permutation_length = 5
    if len(tokens) <= max_permutation_length:
        seen: set[str] = set()
        for perm in itertools.permutations(tokens):
            candidate = "_".join(perm)
            if candidate not in seen:
                seen.add(candidate)
                yield candidate

    # Attempt heuristic organ-quality-state ordering.
    organ_codes = {"SP", "KD", "LV", "HT", "LU", "ST", "GB", "BL"}
    qualities = {"QI", "BLOOD", "YIN", "YANG", "JING", "PHLEGM", "DAMP"}
    states = {"DEF", "STAG", "STASIS", "HEAT", "FIRE", "COLD", "DRY"}

    organ = next((token for token in tokens if token in organ_codes), None)
    quality = next((token for token in tokens if token in qualities), None)
    state = next((token for token in tokens if token in states), None)

    heuristics = []
    if organ and quality and state:
        heuristics.append((organ, quality, state))
    if quality and state and not organ:
        heuristics.append((quality, state))
    if organ and state and not quality:
        heuristics.append((organ, state))
    if organ and quality and not state:
        heuristics.append((organ, quality))

    for combo in heuristics:
        candidate = "_".join(combo)
        yield candidate


def _resolve_code(code: str) -> str:
    """Return the canonical pattern code for *code* or raise an error."""

    tokens = _normalise_tokens(code)
    if not tokens:
        raise UnknownPatternError("Cannot decode an empty pattern name.")

    for candidate in _candidate_codes(tokens):
        if candidate in _PATTERN_DATA:
            return candidate

    raise UnknownPatternError(
        f"Unknown TCM pattern '{code}'. Available patterns: "
        + ", ".join(sorted(_PATTERN_DATA))
    )


def decode_pattern(code: str) -> TCMPattern:
    """Return the :class:`TCMPattern` corresponding to *code*.

    The lookup is case-insensitive and tolerant of spaces, hyphens, or common
    pinyin fragments.  Examples::

        >>> decode_pattern("Spleen qi deficiency")
        TCMPattern(code='SP_QI_DEF', ...)

        >>> decode_pattern("gan-qi-yu")  # Liver qi stagnation in pinyin
        TCMPattern(code='LV_QI_STAG', ...)
    """

    if not isinstance(code, str):
        raise TypeError("Pattern code must be a string.")
    canonical = _resolve_code(code)
    return _PATTERN_DATA[canonical]


def decode_sequence(sequence: str, *, unique: bool = False) -> List[TCMPattern]:
    """Decode a delimited *sequence* of pattern codes.

    Parameters
    ----------
    sequence:
        Text containing one or more pattern identifiers separated by commas,
        semicolons, slashes, or plus signs.
    unique:
        If ``True`` duplicates are removed while preserving the order of
        first appearance.
    """

    if not isinstance(sequence, str):
        raise TypeError("Pattern sequence must be a string.")

    parts = [part.strip() for part in re.split(r"[,;+/]+", sequence) if part.strip()]
    patterns: List[TCMPattern] = []
    seen: Dict[str, None] = {}
    for part in parts:
        canonical = _resolve_code(part)
        if unique and canonical in seen:
            continue
        seen[canonical] = None
        patterns.append(_PATTERN_DATA[canonical])
    return patterns


def available_patterns(*, include_details: bool = False) -> List[str]:
    """Return the list of known pattern codes.

    Parameters
    ----------
    include_details:
        When ``True`` the resulting strings include the human readable name in
        the form ``"CODE – Name"``.  The dash uses an en dash to improve
        readability in rendered documentation.
    """

    codes = sorted(_PATTERN_DATA)
    if not include_details:
        return codes
    return [f"{code} – {_PATTERN_DATA[code].name}" for code in codes]


def search_patterns(keyword: str) -> List[TCMPattern]:
    """Return patterns whose textual fields contain *keyword*.

    The search is case-insensitive and scans across the pattern name,
    description, symptoms, and treatment principle.  Results are returned in
    alphabetical order of their codes for determinism.
    """

    if not isinstance(keyword, str):
        raise TypeError("Search keyword must be a string.")
    if not keyword:
        return []
    matches = [pattern for pattern in _PATTERN_DATA.values() if pattern.matches_keyword(keyword)]
    return sorted(matches, key=lambda pattern: pattern.code)


def explain_pattern(code: str) -> str:
    """Return a human readable multi-line explanation for *code*."""

    pattern = decode_pattern(code)
    symptoms = ", ".join(pattern.key_symptoms)
    explanation = (
        f"{pattern.name} ({pattern.code})\n"
        f"Organ: {pattern.organ} | Element: {pattern.element}\n"
        f"Description: {pattern.description}\n"
        f"Key symptoms: {symptoms}\n"
        f"Treatment principle: {pattern.treatment_principle}"
    )
    return explanation

