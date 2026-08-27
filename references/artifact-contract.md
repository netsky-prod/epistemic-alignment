# Alignment dossier contract

Work under `alignment/`. `manifest.yaml` records the project, current phase, and `snapshot_paths`; `review-state.json` is process state. Read the manifest and existing files before continuing.

| Phase | Source files | Required output |
| --- | --- | --- |
| Discover | charter, stakeholders, glossary, assumptions, open-questions | distinguish facts, statements, inferences, assumptions, contradictions, questions |
| Use cases | `use-cases/UC-*.md` | Cockburn use cases linked to discovery |
| Behavior | `features/*.feature` | observable BDD examples linked to use cases |
| Architecture | `architecture/*.md`, `decisions/ADR-*.md` | C4 views and material decisions |
| Review | `review.md` | human-readable findings and disposition |
| Presentation | `alignment-review/` | derived review view and issued snapshot |
| Handoff | `handoff.md` | only after thin-gate approval |

Use stable, readable IDs where they aid navigation. Keep uncertainty labelled in the source documents. Generated presentation output is never canonical.

## Snapshot membership

The mandatory snapshot membership invariant is file integrity: every human-authored, reviewable dossier file created, renamed, or deleted by a skill must be added, updated, or removed in `manifest.yaml` `snapshot_paths` in the same stage. This includes `use-cases/UC-*.md`, `features/*.feature`, `decisions/ADR-*.md`, and revised reviewable source files. Before issuing or reissuing review, verify every current reviewable dossier file is listed in `snapshot_paths`.

`review-state.json`, generated `handoff.md`, generated presentation output, and temporary or lock files remain excluded. This membership check does not judge document meaning.
