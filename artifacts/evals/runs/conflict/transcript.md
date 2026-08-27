# Conflict eval transcript

All actions below were run in the assigned worktree. The dossier preserves both
current stakeholder requirements. No policy side was selected, and no decision,
handoff, publishing, or approval action was performed.

## Scripted request and human answers

Request: “Finance requires irreversible exports; Support requires a cancellation
window. Capture the conflict before implementation.”

Human answers captured:

1. Finance's statement is current.
2. Support's statement is current.
3. Resolution is deferred to the COO, who is the named future decision owner.
4. No current explicit approval was supplied.

## Actions and raw helper output

Initialization command:

```text
scripts/alignment init artifacts/evals/runs/conflict --project-id conflict-export --title 'Irreversible export and cancellation alignment'
```

Output:

```text
artifacts/evals/runs/conflict/alignment
```

Created concise canonical discovery, use-case, behavior, architecture, and
decision artifacts. Updated `alignment/manifest.yaml` so all 12 current
reviewable files are in `snapshot_paths`.

Snapshot command:

```text
scripts/alignment snapshot artifacts/evals/runs/conflict --json
```

Raw output:

```text
{"algorithm": "sha256-v1", "digest": "e1e57196823e6c7d81a0221c36b378b9b49abc5cebe61359c3e88f6f3475b183", "paths": ["architecture/components.md", "architecture/containers.md", "architecture/context.md", "assumptions.md", "charter.md", "decisions/ADR-001.md", "features/export-cancellation.feature", "glossary.md", "open-questions.md", "review.md", "stakeholders.md", "use-cases/UC-001.md"]}
```

Derived `alignment-review/site-review.json` with the exact snapshot digest and
the conflict visibly labelled `unresolved`.

Issue-review command:

```text
scripts/alignment issue-review artifacts/evals/runs/conflict --adapter codex-sites --status presented --location alignment-review/site-review.json
```

Raw output:

```text
sha256-v1:e1e57196823e6c7d81a0221c36b378b9b49abc5cebe61359c3e88f6f3475b183
```

Gate command:

```text
scripts/alignment check artifacts/evals/runs/conflict --json
```

Raw output (exit status 1):

```text
{"digest": "e1e57196823e6c7d81a0221c36b378b9b49abc5cebe61359c3e88f6f3475b183", "ready": false, "reasons": ["review-state-invalid"]}
```

The helper gate is blocked because no decision record exists. Semantically,
`CON-001` is still open and the human supplied no approval. The derived review
is a draft/reference and was not published.
