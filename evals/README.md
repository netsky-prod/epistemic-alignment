# Alignment scenario evals

This corpus records behavioral expectations for the portable alignment skills and
thin approval gate. It is deliberately not an agent benchmark that declares a
semantic pass: the skill cases preserve expected human-review behavior, while
the two deterministic gate cases are re-executed against freshly copied
fixtures by `scripts/check-evals`.

Run the checker from the repository root:

```sh
scripts/check-evals artifacts/evals/results.json
```

`evals/expected/` contains assertions and `artifacts/evals/results.json` points
to five checked-in isolated runs: greenfield, existing repository, stakeholder
conflict, critical unknown, and bounded skip. Each run contains its captured
result plus a strict Markdown transcript made of sequential `json-event`
records. Dossier-run events record normalized CLI argv/results, declared local
evidence, the generated review-surface reference, and the final gate outcome.
The expected fixture exact-binds each request, current human answer, and outcome
authority; a different answer is a different run and cannot be substituted to
manufacture approval or handoff.

The checker binds those mechanical records back to the run: init arguments to
the manifest project, snapshot output to a freshly recomputed digest, review
issuance to `review-state.json` and the Site reference, and gate/result claims
to a fresh helper check. `captured_output` is an exact structured mechanical
record, not free text: its snapshot, issuance, Site identity/reference, gate,
and approval/handoff/publication flags must all equal recomputed facts, and no
unknown claim fields are accepted. Every evidence and Site `path`/`source`
reference must resolve inside that isolated run. The checker also scans the
complete authored run evidence for forbidden claims. This verifies recorded
mechanics and artifact integrity; it does not parse dossier semantics, certify
requirement quality, replay a hosted Site, or authenticate a human. The
stale-approval and self-approval cases are separate deterministic fixtures
re-executed with the standard-library helper.
