# Thin approval gate

The CLI records process integrity only. It does not assess the dossier's meaning.

Resolve `ALIGNMENT_HELPER` from the installed plugin as described in [installed resources](installed-resources.md). The human never runs these commands.

1. Create the current snapshot: `"$ALIGNMENT_HELPER" snapshot "$PROJECT_ROOT" --json`.
2. After a review view exists, issue it: `"$ALIGNMENT_HELPER" issue-review "$PROJECT_ROOT" --adapter <adapter> --status presented --location <reference>`.
3. Show the stakeholder the view reference, `alignment/review.md`, its findings, and the issued hash.
4. Ask for a simple `approved`, `changes_requested`, or `rejected` reply. The human does not need to copy the hash. Bind the explicit current reply internally to the current issued hash, then transcribe it using `"$ALIGNMENT_HELPER" decide "$PROJECT_ROOT" --decision approved --reviewer <label> --provenance human-message --review-hash <hash> --acknowledged-finding ID`. Repeat `--acknowledged-finding ID` only for findings the human explicitly accepts.
5. Run `"$ALIGNMENT_HELPER" check "$PROJECT_ROOT" --json`, then `"$ALIGNMENT_HELPER" handoff "$PROJECT_ROOT"` only when ready. Read the handoff and dossier, then check again immediately before Superpowers brainstorming.

Any included-file change makes approval stale. `changes_requested` returns work to its relevant phase; `rejected` ends the attempt without handoff. A button, silence, generic earlier permission, agent confidence, or edited state is not a decision.

Never replay a prior human message after a new review issuance. Never make the human copy a digest merely to satisfy the helper interface.

After handoff generation, `review-state.json` binds the exact helper-written
`handoff.md` bytes with `handoff.content_sha256`. A handoff file without a
complete record, a record without the file, malformed or mismatched hashes,
non-regular files, symlinks, and interrupted handoff transactions all fail
closed. Never repair this state by editing hashes or substituting a file.
