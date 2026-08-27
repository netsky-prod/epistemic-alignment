# Thin approval gate

The CLI records process integrity only. It does not assess the dossier's meaning.

1. Create the current snapshot: `scripts/alignment snapshot <root> --json`.
2. After a review view exists, issue it: `scripts/alignment issue-review <root> --adapter <adapter> --status presented --location <reference>`.
3. Show the stakeholder the view reference, `alignment/review.md`, its findings, and the issued hash.
4. Transcribe only a current explicit human message using `scripts/alignment decide <root> --decision approved --reviewer <label> --provenance human-message --review-hash <hash> --acknowledged-finding ID`. Repeat `--acknowledged-finding ID` for each acknowledged finding.
5. Run `scripts/alignment check <root>`, then `scripts/alignment handoff <root>` only when the current snapshot is ready.

Any included-file change makes approval stale. `changes_requested` returns work to its relevant phase; `rejected` ends the attempt without handoff. A button, silence, generic earlier permission, agent confidence, or edited state is not a decision.
