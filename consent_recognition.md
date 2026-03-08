# Consent Recognition

Consent recognition is the practice of detecting, confirming, and continuously respecting a person’s permission in human interactions and digital systems. It is not just a one-time checkbox; it is an ongoing process that must be understandable, reversible, and context-aware.

## Core principles

1. **Clarity**: Consent requests should be plain-language, specific, and free of coercion.
2. **Specificity**: People should be able to approve one action while declining another.
3. **Revocability**: Consent can be withdrawn at any time, and systems should honor withdrawal quickly.
4. **Verifiability**: Decisions should be auditable without exposing unnecessary personal data.
5. **Accessibility**: Prompts and controls should work for diverse languages, literacy levels, and abilities.

## Signals of valid consent

- Explicit affirmative action (e.g., signed form, verbal yes, deliberate opt-in click).
- Context alignment (the request matches the stated purpose and scope).
- Capacity and voluntariness (no pressure, deception, or inability to decide).
- Temporal relevance (consent is recent enough for the action being taken).

## Red flags

- Pre-checked boxes or dark patterns.
- Bundled permissions that force unrelated acceptance.
- Ambiguous wording or hidden consequences.
- Missing or difficult withdrawal mechanism.

## Implementation pattern for systems

1. Present purpose-limited consent options in clear language.
2. Capture proof of consent (timestamp, version, scope, actor).
3. Enforce policy checks before any action using that consent.
4. Offer one-step review and revocation.
5. Log decisions and policy outcomes for accountability.

## Example policy checks

- Is the consent still active?
- Does the requested action fit the approved scope?
- Is the requester authorized for the stated purpose?
- Has the user withdrawn or modified consent since the last check?

## Why it matters

Strong consent recognition improves trust, reduces legal and ethical risk, and protects personal autonomy. In healthcare, education, finance, and AI systems, it is a foundational safeguard for dignity and safety.
