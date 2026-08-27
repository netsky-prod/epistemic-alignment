---
name: align-project
description: Use when a software initiative is ambiguous, architecture-changing, stakeholder-heavy, risky, or large enough that implementation should not begin before shared understanding is established.
---

# Align Project

Run epistemic alignment before implementation planning. The goal is not more documentation; it is a shared, inspectable model of the problem that exposes disagreement while it is still cheap to resolve.

## Contract

Input: absolute project root, human request, repository evidence, and any existing `alignment/` dossier.

Output: either a concise bounded-work skip rationale, or an initialized/resumed dossier and exactly one next skill.

Read [installed resources](../../references/installed-resources.md) and [the dossier contract](../../references/artifact-contract.md). Resolve bundled resources from this skill's installed path, never from the target project's working directory. Keep plugin root and project root separate.

## Decide whether alignment is warranted

Use the workflow when any of these is true:

- material ambiguity or competing interpretations;
- behavior crosses teams, systems, trust boundaries, or public interfaces;
- architecture, persistence, security, migration, or operations may change;
- multiple stakeholders carry different goals or failure costs;
- incorrect assumptions would cause expensive rework;
- the human explicitly requests alignment, use cases, BDD, C4, or stakeholder review.

Skip only genuinely bounded work whose expected behavior and affected surface are already clear. Record `bounded-work skip` and the reason in `charter.md`; produce no approval or handoff. A small diff does not by itself make the problem bounded.

## Start or resume

1. Resolve the bundled helper and absolute target root.
2. If the dossier is absent, run `"$ALIGNMENT_HELPER" init "$PROJECT_ROOT" --project-id <stable-id> --title <human title>`.
3. Read `manifest.yaml` and every existing dossier artifact before asking questions. Files are restart authority; conversation memory is advisory.
4. Determine the first incomplete phase from actual artifacts. A phase is incomplete when required output is absent, still a blank template, explicitly unfinished, internally contradicted, or invalidated by a later change.
5. Reconcile phase metadata without erasing useful work. Files win when metadata is stale.

## Epistemic discipline

Keep these categories distinct:

- observed fact — directly supported by repository, system, policy, or supplied source;
- stakeholder statement — what a named person or group says or wants;
- inference — the agent's interpretation;
- assumption — a provisional proposition used without adequate evidence;
- contradiction — claims or constraints that cannot all hold as written;
- open question — missing information that can change behavior or architecture;
- decision — an explicit choice with owner and consequences.

Never silently promote one category into another. When sources disagree, preserve both claims, name the conflict, and identify decision authority.

## Question loop

Ask one material question at a time. Choose the question with the largest expected effect on scope, stakeholder outcome, irreversible architecture, or risk. Do not ask for information already present in the repository.

After each answer:

1. update the relevant canonical artifact;
2. record whose statement it is and supporting evidence;
3. update linked assumptions, contradictions, and questions;
4. summarize what changed in the model;
5. continue only if the next question remains material.

If the human does not know, record that honestly and identify an owner, evidence source, experiment, or explicitly reversible proposed assumption.

## Resume routing

- discovery incomplete → `alignment:discover-domain`
- goals known but Cockburn use cases incomplete → `alignment:write-use-cases`
- priority paths lack observable examples → `alignment:specify-behavior`
- responsibilities or material choices are unexplained → `alignment:model-architecture`
- cross-artifact review is absent or stale → `alignment:review-alignment`
- stakeholder presentation is absent or stale → `alignment:build-review`
- current presentation awaits decision or verified handoff delivery → `alignment:approve-handoff`

Before transition, synchronize `snapshot_paths`, `completed_phases`, and `current_phase`. Artifacts remain authoritative if phase metadata later drifts.

## Stop conditions

Stop when a missing human choice would materially alter the result, evidence is unavailable, or stakeholder authority is unclear. Report the blocker and affected artifacts. Do not turn alignment into implementation design, task decomposition, or code generation; those begin after the approved handoff enters `superpowers:brainstorming`.

Final response: current phase, what is established, the most consequential uncertainty, files changed, and the one next skill.
