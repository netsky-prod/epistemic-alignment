# Independent `alignment:specify-behavior` invocation

Date: 2026-08-28 (Europe/Moscow)

This is a real, isolated application of one shipped skill to a disposable copy
of the committed `input/` fixture. It is evidence of the skill's independent
I/O mechanics, not a semantic evaluator or certificate. The authoritative
approved example and eval runs were excluded from the actor's scope and were
not modified.

## Invocation

- Runtime: `codex-cli 0.148.0-alpha.9`
- Fresh ephemeral thread: `01a04508-d786-7a50-92b6-9008ef551f0e`
- Sandbox: `workspace-write`
- Disposable worktree-local fixture: `.task8-specify.sVTLK3` (removed after capture)
- Allowed package inputs: `skills/specify-behavior/SKILL.md` and its required
  `references/bdd.md`
- Dossier input: the files under `input/alignment/`

Exact task prompt:

> You are a fresh-context actor performing a bounded independent-skill
> invocation exercise. Use only the fixture in your current working directory
> and the shipped alignment:specify-behavior skill, plus the single method
> reference that skill explicitly requires. Do not read or invoke align-project
> or any other alignment skill. Do not read the authoritative approved example
> or any eval run. Read the specify-behavior skill completely, inspect the
> fixture inputs, and actually apply it: create the required
> alignment/features/*.feature output and update alignment/manifest.yaml
> snapshot_paths for that output. The fixture supplies every material
> observable input, so do not ask a question. Keep scope at behavior only; do
> not create architecture, APIs, algorithms, tests, approval, review state, or
> handoff. Use apply_patch for edits. At the end, report the input files read,
> files created/modified, and next transition.

## Actor transcript

The actor read the requested skill, its required BDD reference, and exactly the
six fixture inputs. Before editing it reported:

> The observable scope is fully specified, so no question is needed. I'll
> capture the confirmed success and duplicate-request behavior, plus the
> proposed ineligible-review boundary linked to `ASM-102`, all under `UC-101`.

The recorded file-change event added
`alignment/features/expedited-refund.feature` and updated
`alignment/manifest.yaml`. The actor then parsed the JSON-compatible manifest,
ran whitespace validation, reread both changed files, and reported:

> Created the behavioral specification and synchronized the manifest.
>
> Files changed:
>
> - Created `alignment/features/expedited-refund.feature`
> - Modified `alignment/manifest.yaml` to add its snapshot path
>
> Next transition: `alignment:model-architecture`.

## Mechanical and manual inspection

The input snapshot did not contain a feature path. The captured result contains
the new `.feature` file and adds exactly `features/expedited-refund.feature` to
`snapshot_paths`; the before/after digests and file hashes are recorded in
`provenance.json` and reproduced by the release test.

Manual inspection confirmed that the captured output is a Gherkin artifact,
keeps the proposed criterion visibly proposed, and contains no architecture,
API, algorithm, test-framework, review-state, approval, or handoff artifact.
That inspection is human evidence only; no Gherkin parser or semantic checker
was added.
