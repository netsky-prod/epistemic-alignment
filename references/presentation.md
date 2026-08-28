# Stakeholder presentation method

A review surface is successful when a stakeholder can form an accurate mental model, locate the evidence behind important claims, see uncertainty and disagreement, and understand the decision being requested.

## Narrative order

1. Problem, desired outcome, scope, and non-goals.
2. Stakeholders, interests, authority, and conflicts.
3. Priority use cases with success/minimal guarantees.
4. Concrete behavior examples and meaningful boundaries.
5. C4 responsibilities and material ADRs.
6. Risks, assumptions, contradictions, and open questions.
7. Independent findings and their dispositions.
8. Review-binding mode, downstream-rigor recommendation, and the precise approval boundary.

## Evidence entry

For each material claim show:

```text
Source: <path or stable ID>
Status: confirmed | proposed | assumed | conflicting | open
Excerpt: <substantive, faithful human-readable evidence>
Related: <goal / UC / SCN / C4 / ADR / finding IDs>
```

An evidence link that only repeats its source label is insufficient. The target must let the stakeholder inspect the cited substance without pretending the derived copy is canonical.

## Communication rules

- Put findings before readiness.
- Never use color as the only status signal.
- Pair diagrams with text and responsibility tables.
- Separate accepted limitations from resolved findings.
- State what approval unlocks and what remains undecided.
- Show which downstream gates are recommended or omitted and the risks that justify that choice.
- Optimize for stakeholder comprehension, not dossier completeness on one screen.
- Keep the surface read-only; decisions stay in the human conversation.
