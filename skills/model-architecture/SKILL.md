---
name: model-architecture
description: Use when alignment use cases and behavior examples need C4 views and material architecture decisions explained for stakeholder review.
---

# Model Architecture

Explain how responsibilities support required behavior and where choices carry consequences.

## Contract

Input: discovery, use cases, behavior examples, and relevant repository facts. Output: C4 Markdown views under `alignment/architecture/` and material `alignment/decisions/ADR-*.md`. Read [the C4 and ADR recipe](../shared/references/c4.md).

1. Inspect existing architecture views, ADRs, use cases, and scenarios; resume the first behavior whose responsibility has no explanation.
2. Write system context for a software system. Add containers when deployables or stores matter; add components only where internal structure affects material behavior or a decision.
3. Pair each Mermaid view with a responsibility table linking elements to use cases/scenarios and open concerns.
4. Create one ADR for each material choice, including context, decision, consequences, and alternatives. Ask one material question when a choice or its consequence is unknown.
5. Preserve contradictions, assumptions, and unknowns as visible concerns.

Do not imply that a diagram settles an undecided responsibility. Next transition: `alignment:review-alignment`.
