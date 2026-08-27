# Workflow application evidence

Date: 2026-08-27

These are read-only, fresh-context applications of the shipped skills. They
exercise resume and unavailable-transition behavior without adding an
evaluator or semantic release gate. No application in this file modified
dossier, approval, handoff, or repository state.

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

## Independent skill invocation

The earlier read-only prediction has been superseded by a real isolated
`alignment:specify-behavior` invocation with committed input, produced output,
manifest membership change, transcript, provenance, manual inspection, and a
mechanical replay regression. See
[`skill-invocations/specify-behavior/`](skill-invocations/specify-behavior/).

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
