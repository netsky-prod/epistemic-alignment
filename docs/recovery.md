# Recovery

The workflow is restartable through files. Inspect `alignment/manifest.yaml`,
the dossier, `alignment/review.md`, `alignment/handoff.md`, and the process
contract; do not rely on conversation memory. Inspect `review-state.json` only
for exact-snapshot binding.

## Interrupted authoring

Reinvoke `alignment:align-project`. It resumes at the first incomplete phase.
Preserve confirmed material, identify inferred or uncertain text explicitly,
and continue with one material question at a time. If initialization was
interrupted before `alignment/` existed, rerun `scripts/alignment init`. If the
directory already exists, the initializer safely refuses to overwrite it.

## Exact-snapshot or manifest failure

This section applies only to exact-snapshot binding.

Run:

```sh
scripts/alignment snapshot <project-root> --json
```

Correct only the file named by the error: a missing, duplicate, unsafe,
escaping, non-file, or invalid UTF-8 `snapshot_paths` entry. Do not add or
remove paths merely to force a desired digest. Ensure every current reviewable
dossier file is included, then rebuild the presentation and issue a fresh
review.

## Stale decision

A material source/finding change invalidates conversational approval. Return to
semantic review, rebuild the presentation, show the changed decision context,
and obtain a current human reply.

In exact-snapshot mode, any included-file edit after issuance invalidates
approval. Do not restore an old hash, edit `review-state.json`, or copy a prior
handoff.

1. Rerun semantic review for the changed dossier.
2. Rebuild the Site payload from the new snapshot.
3. Visually inspect desktop and narrow layouts.
4. Issue the new exact digest.
5. Show the findings and digest to the stakeholder again.
6. Obtain a new explicit decision in the current interaction.
7. Run `check`, then regenerate the handoff.

## Changes requested or rejected

For `changes_requested`, return to the relevant authoring phase, preserve the
decision record as history until the next issuance resets it, and follow the
fresh-review steps above. For `rejected`, close the attempt without a handoff.
Never reinterpret either outcome as approval.

## Site build or publication failure

The dossier remains canonical. A build, inspection, hosting, or update failure
must not mutate it or mark presentation complete. Fix the derived Site and
rebuild. If its represented dossier or digest changes, issue a fresh review.
Publication is optional and consent-gated; a local presented review is valid
when the stakeholder has actually been shown it.

## Exact-snapshot handoff interruption

This section applies only to exact-snapshot binding. A conversational handoff
is recovered by rereading its named sources and re-presenting if material
content changed.

Rerun `scripts/alignment check <project-root> --json`. The helper fails closed
if an approval transaction is unresolved, if the handoff file/state disagree,
if the handoff is a symlink or non-regular file, if its exact bytes do not match
the recorded `content_sha256`, or if the snapshot changed. A leftover
`.handoff-pending` or `.handoff-backup` means an interrupted transaction; keep
it fail-closed while inspecting whether the prior handoff must be restored.
Never delete transaction evidence blindly, edit hashes, or substitute a file.
Once the mechanical state is resolved and `ready` is true, rerun
`scripts/alignment handoff`.

## Installed plugin not refreshing

Use the cachebuster and reinstall flow in [installation](installation.md), then
start a new Codex task. Do not edit marketplace JSON or Codex configuration by
hand. If a non-default marketplace no longer points to a local source, stop and
repair that marketplace mapping before reinstalling.
