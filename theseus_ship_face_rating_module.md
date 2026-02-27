# Theseus’ Ship Face Rating Module

A compact framework for evaluating whether an entity still “looks like itself” after incremental change.

## Purpose

The **Theseus’ Ship Face Rating Module** measures perceived identity continuity when parts, features, or behaviors are replaced over time.

It does **not** answer metaphysical identity conclusively. It provides a practical scoring lens for design reviews, product evolution, and narrative analysis.

## Core question

> At what point does a thing stop presenting the same recognizable “face”?

## Rating dimensions (0–5 each)

1. **Visual continuity**  
   Are high-salience surface traits still recognizable?
2. **Structural continuity**  
   Is the underlying architecture preserved?
3. **Behavioral continuity**  
   Does it act in familiar ways under normal conditions?
4. **Memory/trace continuity**  
   Are records, state, or lineage links retained?
5. **Narrative continuity**  
   Do observers still tell one coherent story about it?

## Composite score

- **Total score:** sum of five dimensions (0–25).
- **Interpretation bands:**
  - **21–25:** Strong same-face continuity
  - **16–20:** Mostly same face, with notable drift
  - **10–15:** Ambiguous identity presentation
  - **0–9:** Face discontinuity likely

## Quick protocol

1. Define the baseline version (“Ship at T0”).
2. Identify changed components since T0.
3. Score each dimension 0–5.
4. Add scores and map to interpretation band.
5. Record disagreements between evaluators; re-score after discussion.

## Example (brief)

A product UI keeps layout and interaction model but swaps visuals and backend state format.

- Visual continuity: 3
- Structural continuity: 4
- Behavioral continuity: 5
- Memory/trace continuity: 2
- Narrative continuity: 4

**Total:** 18/25 → Mostly same face, with notable drift.

## When to use

- Version-to-version product reviews
- Brand redesign governance
- AI model lineage communication
- Fiction/worldbuilding consistency checks

## Limitation note

This module captures *perceived continuity*, not legal ownership, moral status, or ontological truth.
