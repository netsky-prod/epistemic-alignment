---
name: align-project
description: Use when a new, ambiguous, architecture-changing, stakeholder-heavy, or materially risky software initiative needs shared understanding before implementation planning.
---

# Align Project

Create or resume the dossier; the files, not conversation memory, define progress.

## Contract

Input: project root and the human's request. Output: either a recorded skip rationale or an initialized/resumed `alignment/` dossier with its next phase identified. Read [the dossier contract](../../references/artifact-contract.md).

1. Inspect `alignment/manifest.yaml` if it exists. Otherwise qualify the request: use alignment for substantial scope, ambiguity, architectural/public-interface change, multiple stakeholders, or material risk. For bounded work, record a short rationale in `charter.md` and produce neither approval nor handoff.
2. Initialize an absent dossier with `scripts/alignment init <root> --project-id <id> --title <title>`.
3. Read the existing phase files and `manifest.yaml`; continue at the first incomplete phase. Sync manifest `snapshot_paths` for every reviewable file created, renamed, or deleted in this stage before transition. Preserve labelled facts, statements, inferences, assumptions, contradictions, and questions.
4. Ask one material question at a time when the files cannot answer it. Keep the current phase honest rather than inventing certainty.

Resume mapping: `discover` → `alignment:discover-domain`; `use-cases` → `alignment:write-use-cases`; `behavior` → `alignment:specify-behavior`; `architecture` → `alignment:model-architecture`; `review` → `alignment:review-alignment`; `presentation` → `alignment:build-review`; `approval` → `alignment:approve-handoff`.

Do not turn the dossier into implementation planning or derive approval from readiness. Next transition: invoke the mapped skill for the first incomplete phase.
