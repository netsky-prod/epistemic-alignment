# Human decision and handoff

Approval means the reviewed dossier is an adequate basis for downstream brainstorming. It does not certify semantics, security, estimates, identity, or implementation correctness.

The process contract selects one of two bindings. Do not silently upgrade from conversational to exact-snapshot merely because tooling exists.

## Conversational binding — default

Use when review and downstream brainstorming occur in a continuous human interaction and no material need for exact-byte provenance exists.

1. Show the review surface, `alignment/review.md`, open findings, accepted limitations, and the downstream-rigor recommendation.
2. Ask for one explicit current decision: `approved`, `changes_requested`, or `rejected`.
3. On approval, write a human-readable `alignment/handoff.md` naming the presentation reference, reviewed source paths, reviewer label, current-message provenance, accepted findings, remaining uncertainty, and recommended downstream rigor.
4. Read the current sources once more before delivery. A material change requires re-presentation and a new decision.

Do not claim cryptographic freshness, authenticated identity, or exact-byte binding in this mode.

## Exact-snapshot binding — opt in

Use only when the process contract names a real need: version-bound approval requested by the human, regulated/audited evidence, asynchronous or multi-writer review with material stale-version risk, or difficult-to-reverse downstream action.

Resolve `ALIGNMENT_HELPER` from the installed plugin as described in [installed resources](installed-resources.md). The human never runs these commands.

1. Create the current snapshot: `"$ALIGNMENT_HELPER" snapshot "$PROJECT_ROOT" --json`.
2. Issue the rendered review: `"$ALIGNMENT_HELPER" issue-review "$PROJECT_ROOT" --adapter <adapter> --status presented --location <reference>`.
3. Show the view, findings, and issued digest. The human does not copy the digest.
4. Bind only a current explicit human reply using `"$ALIGNMENT_HELPER" decide "$PROJECT_ROOT" --decision approved --reviewer <label> --provenance human-message --review-hash <hash> --acknowledged-finding ID`.
5. Run `check`, generate `handoff`, read the handoff and dossier, then run `check` again immediately before Superpowers brainstorming.

Any included-file change makes exact-snapshot approval stale. Never replay a prior human message after a new issuance, edit hashes, substitute handoff files, or treat the helper as semantic proof.

## Authority in both modes

A button, silence, generic earlier permission, agent confidence, a test fixture, or approval of the plugin design is not approval of the presented dossier. `changes_requested` returns to the earliest materially affected phase; `rejected` ends the attempt without handoff.
