# Variable Framing

Variable framing is the practice of choosing how a variable is defined, measured, and interpreted before analysis begins. The same underlying phenomenon can produce very different conclusions depending on this framing.

## Core idea
A variable is never just a number. It is a design choice:
- **Definition:** What exactly counts as the thing being measured?
- **Unit and scale:** Is it binary, ordinal, continuous, log-scaled, or normalized?
- **Context window:** Over what time, place, population, or condition is it measured?
- **Reference point:** Compared to what baseline or control?

## Why it matters
- **Shapes conclusions:** Different framings can invert trends or hide effects.
- **Affects fairness:** Labels and thresholds can advantage or disadvantage groups.
- **Controls actionability:** Badly framed variables lead to decisions that are hard to implement.
- **Impacts reproducibility:** Clear framing makes studies and models easier to replicate.

## Practical checks
1. Write an explicit one-sentence variable definition.
2. List excluded cases and edge conditions.
3. Test at least one alternative framing and compare results.
4. Report sensitivity to scaling, binning, and baseline choices.
5. Document the framing rationale in plain language.

## Quick example
Suppose a team tracks "student success."
- **Framing A:** exam score above 70.
- **Framing B:** semester-to-semester improvement.
- **Framing C:** completion of core competencies.

Each framing answers a different question. None is universally correct; the best one depends on the decision the metric is meant to support.

## Bottom line
Good analysis is not only about modeling technique. It begins with variable framing that is explicit, justified, and matched to the real-world question.
