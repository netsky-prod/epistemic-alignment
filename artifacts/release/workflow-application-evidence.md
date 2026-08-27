# Workflow application evidence

Date: 2026-08-27

These are read-only, fresh-context applications of the shipped skills. They
exercise skill behavior without adding an evaluator or semantic release gate.
No application modified dossier, approval, handoff, or repository state.

## Restart from files

Scenario: conversation context is lost; discovery documents and
`alignment/use-cases/UC-001.md` are complete; `alignment/features/` has no
scenario; architecture files remain untouched templates; the manifest phase is
stale at `discover`.

Observed output:

> The first incomplete phase is **behavior**.
>
> Exact next transition: `alignment:specify-behavior`.
>
> Reason: discovery files and `alignment/use-cases/UC-001.md` are complete, but
> `alignment/features/` contains no `.feature` scenario. The architecture files
> remain untouched templates, so architecture has not started. The stale
> `manifest.yaml` value `current_phase: discover` does not override the dossier
> evidence; files define progress.

## Independent skill invocation and boundary

Scenario: invoke `alignment:specify-behavior` directly with completed discovery
files and `alignment/use-cases/UC-001.md`, without `align-project` or prior
conversation.

Observed output:

> Input boundary: completed discovery context,
> `alignment/use-cases/UC-001.md`, and its confirmed or proposed criteria.
>
> Output boundary: linked, reviewable Gherkin behavior only—no APIs,
> algorithms, architecture, or test mechanics.
>
> Artifact: `alignment/features/uc-001.feature`, containing `alignment-meta`
> with `"use_case":"UC-001"` and `"status":"proposed"`, stable
> `@SCN-* @UC-001` tags, an applicable `Rule`, the main observable success
> path, and any outcome-changing failure/recovery scenario. Assumptions and
> unresolved questions remain linked rather than guessed away.
>
> Snapshot action: add `features/uc-001.feature` to
> `alignment/manifest.yaml`'s `snapshot_paths`.
>
> Next transition: `alignment:model-architecture`.

## Superpowers-unavailable delivery

Scenario: a current human approved the issued snapshot, the gate returned
ready, `/tmp/release/alignment/handoff.md` was generated and verified, and
`superpowers:brainstorming` is unavailable.

Before the conditional guidance, the fresh-context baseline output was:

> Next, transition to `superpowers:brainstorming`, supplying the verified
> `handoff.md` and dossier. Because that skill is unavailable, I stop and report
> the blocked transition; I do not substitute another workflow.
>
> I mutate nothing: no scripts are rerun, and no files or review state are
> changed.

This preserved state but unconditionally attempted the transition and omitted
the required pending-delivery shape: no `delivery pending` status, no exact
handoff path, and no later-resume instruction.

With the conditional guidance, the equivalent fresh-context output was:

> I report delivery pending at `/tmp/release/alignment/handoff.md`. I do not
> regenerate the handoff, rerun alignment scripts, alter `review-state.json`,
> change approval state, or mutate the snapshot or any files. The next action
> is to resume the transition with `handoff.md` and the dossier when
> `superpowers:brainstorming` becomes available.
