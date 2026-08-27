---
name: review-alignment
description: Use when an alignment dossier needs an independent cross-review of goals, use cases, examples, architecture, decisions, and unresolved uncertainty.
---

# Review Alignment

Use human judgment to make semantic gaps visible for stakeholder decision.

## Contract

Input: the complete current `alignment/` dossier. Output: `alignment/review.md` containing evidence-backed, human-readable findings and dispositions. Read [the semantic-review record](../shared/references/semantic-review.md).

1. Read the dossier afresh: discovery, use cases, features, architecture, ADRs, and existing `review.md`. Resume by updating stale or undispositioned findings.
2. Look for unsupported goals, important paths without concrete examples, unexplained responsibilities, decisions without consequences, contradictions, hidden assumptions, and critical unknowns.
3. Write each finding with an ID, evidence path/ID, impact, suggested owner, and open/accepted/resolved disposition. Preserve the review scope and limits.
4. Ask one material question when a finding cannot be located or characterized from the files. Revisit source documents when a human answer changes them.
5. Sync manifest `snapshot_paths` for every reviewable file created, renamed, or deleted in this stage; verify every current reviewable dossier file is listed before issue-review.

Do not convert findings into a machine-style certificate; `review.md` records human judgment. Next transition: `alignment:build-review`.
