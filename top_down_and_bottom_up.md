# Top-down and bottom-up

## Overview
Top-down and bottom-up are complementary strategies for reasoning, planning, and building systems. Effective teams often blend both: top-down frames the destination while bottom-up discovers the practical path.

## Top-down approach
- **Start with the whole:** Define the overall goal, constraints, and success criteria before diving into details.
- **Decompose:** Break the system into subsystems, interfaces, and milestones.
- **Advantages:** Clear direction, easier alignment across teams, predictable sequencing.
- **Risks:** Can miss ground realities or rely on assumptions that fail during implementation.

## Bottom-up approach
- **Start with components:** Build or study small pieces first, then compose them into larger structures.
- **Iterate and integrate:** Validate behavior early, reusing proven blocks as the design scales.
- **Advantages:** Early empirical feedback, resilience through tested parts, natural innovation from prototypes.
- **Risks:** Can drift without a unifying vision, leading to integration friction or scope creep.

## When to favor each
- Favor **top-down** when the problem is well understood, regulatory or safety constraints are strict, or cross-team alignment is essential.
- Favor **bottom-up** when exploring new domains, reducing technical risk with prototypes, or evolving legacy systems incrementally.

## Hybrid practice
- Start with a lightweight top-down map (goals, interfaces, acceptance tests).
- Run bottom-up spikes to de-risk unknowns and refine estimates.
- Iterate: update the top-down plan based on bottom-up findings, keeping interfaces stable when possible.

## Quick checklist
- **Top-down:** goal defined, constraints captured, interfaces outlined, milestones set.
- **Bottom-up:** reusable components identified, prototypes exercised, integration tests planned, feedback loops scheduled.

## Example: API platform rollout
1. **Top-down:** Set success metrics (latency, availability), design the service boundaries, and define versioning and security models.
2. **Bottom-up:** Build a minimal endpoint with observability, iterate on client SDK prototypes, and validate auth flows with test tenants.
3. **Integrate:** Align SDK learnings with the service contract, expand coverage, and harden SLOs before general availability.

Blending top-down vision with bottom-up evidence yields plans that are both coherent and grounded.
