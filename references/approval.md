# Thin approval gate

The CLI records process integrity only. It does not assess the dossier's meaning.

1. Create the current snapshot: `scripts/alignment snapshot <root> --json`.
2. After a review view exists, issue it: `scripts/alignment issue-review <root> --adapter <adapter> --status presented --location <reference>`.
3. Show the stakeholder the view reference, `alignment/review.md`, its findings, and the issued hash.
4. Ask for a simple `approved`, `changes_requested`, or `rejected` reply. The human does not need to copy the hash. Bind the explicit current reply internally to the current issued hash, then transcribe it using `scripts/alignment decide <root> --decision approved --reviewer <label> --provenance human-message --review-hash <hash> --acknowledged-finding ID`. Repeat `--acknowledged-finding ID` for each acknowledged finding.
5. Run `scripts/alignment check <root>`, then `scripts/alignment handoff <root>` only when the current snapshot is ready.

Any included-file change makes approval stale. `changes_requested` returns work to its relevant phase; `rejected` ends the attempt without handoff. A button, silence, generic earlier permission, agent confidence, or edited state is not a decision.

After handoff generation, `review-state.json` binds the exact helper-written
`handoff.md` bytes with `handoff.content_sha256`. A handoff file without a
complete record, a record without the file, malformed or mismatched hashes,
non-regular files, symlinks, and interrupted handoff transactions all fail
closed. Never repair this state by editing hashes or substituting a file.
