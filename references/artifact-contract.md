# Alignment dossier contract

Work under `alignment/`. Canonical files are written for humans and remain useful after conversation context is lost. `charter.md` records the process contract; `manifest.yaml` records project identity and phase progress. `snapshot_paths` and `review-state.json` are mechanical state only when exact-snapshot binding is selected. Read all existing phase files before continuing.

| Phase | Source files | Required output |
| --- | --- | --- |
| Discover | charter, stakeholders, glossary, assumptions, open-questions | distinguish facts, statements, inferences, assumptions, contradictions, questions |
| Use cases | `use-cases/UC-*.md` | Cockburn use cases linked to discovery |
| Behavior | `features/*.feature` | observable BDD examples linked to use cases |
| Architecture | `architecture/*.md`, `decisions/ADR-*.md` | C4 views and material decisions |
| Review | `review.md` | human-readable findings and disposition |
| Presentation | `alignment-review/` | derived review view and explicit decision boundary |
| Handoff | `handoff.md` | only after a current explicit human decision |

Use stable, readable IDs where they aid navigation. Keep uncertainty labelled in the source documents. Generated presentation output is never canonical.

## Phase metadata

When a phase declares its next transition, add the finished phase to `completed_phases` and set `current_phase` to the next phase. Do not mark a phase complete while a material unanswered question blocks its required output. On restart, actual artifacts override stale metadata; reconcile the manifest rather than discarding work.

A phase may be recorded `not needed` when the process contract names why it would resolve no material decision or risk. Do not create filler artifacts to satisfy the phase table. Revisit a skipped phase only when new evidence activates its purpose.

## Process contract

`charter.md` records deliverables, material risks, reversibility, retained and omitted phases/gates, review-binding mode, downstream-rigor recommendation, and escalation/downgrade triggers. This is a judgment record, not machine policy. Update it when evidence changes in either direction.

## Epistemic conventions

Canonical documents distinguish observed facts, stakeholder statements, agent inferences, assumptions, contradictions, open questions, and explicit decisions. These are readable conventions, not mandatory metadata on every sentence and not inputs to a semantic parser.

Every important claim should be inspectable through a source path, stable ID, named speaker, or explicit `proposed` status. Derived summaries do not become stronger evidence than their source.

## Exact-snapshot membership

This section applies only when the process contract selects `exact-snapshot`. Every human-authored, reviewable dossier file created, renamed, or deleted by a skill must then be added, updated, or removed in `manifest.yaml` `snapshot_paths` in the same stage. This includes `use-cases/UC-*.md`, `features/*.feature`, `decisions/ADR-*.md`, and revised reviewable source files. Before issuing or reissuing review, verify every current reviewable dossier file is listed.

`review-state.json`, generated `handoff.md`, generated presentation output, and temporary or lock files remain excluded. This membership check does not judge document meaning.

## Change propagation

When a source changes, revisit downstream artifacts that depend on it:

- stakeholder goal/constraint → use cases and review;
- use-case guarantee/extension → BDD and architecture;
- behavior/rule → architecture and ADRs;
- architecture responsibility/decision → review and presentation;
- any materially reviewed source after presentation → presentation and human decision become stale;
- any byte change after exact-snapshot issuance → the bound decision becomes stale.

Do not patch only a summary when the canonical source is wrong.
