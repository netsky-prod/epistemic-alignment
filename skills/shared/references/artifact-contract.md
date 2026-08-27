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
