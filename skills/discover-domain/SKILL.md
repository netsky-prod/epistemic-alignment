---
name: discover-domain
description: Use when an alignment dossier needs stakeholder goals, vocabulary, constraints, assumptions, contradictions, or unresolved domain questions clarified.
---

# Discover Domain

Build a reviewable account of what is known, claimed, inferred, and unknown.

## Contract

Input: initialized `alignment/` dossier, repository evidence, approved sources, and human answers. Output: updated discovery files that identify their provenance and uncertainty. Read [the dossier contract](../../references/artifact-contract.md).

1. Inspect `charter.md`, `stakeholders.md`, `glossary.md`, `assumptions.md`, and `open-questions.md`; resume the first incomplete category.
2. Inspect relevant repository evidence without converting implementation details into stakeholder intent.
3. Ask one material question at a time. Record each answer as a stakeholder statement; record an inference separately and mark its confidence.
4. Use clear entries for desired outcomes, constraints, assumptions, contradictions, and open questions. Link related entries by readable IDs where useful.
5. Summarize the current goal, stakeholders, vocabulary, constraints, and material uncertainty in `charter.md`.
6. Sync manifest `snapshot_paths` for every reviewable file created, renamed, or deleted in this stage before transition.

Do not silently resolve a contradiction or promote an inference to fact. Next transition: `alignment:write-use-cases`.
