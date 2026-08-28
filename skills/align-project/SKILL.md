---
name: align-project
description: Use when a software initiative is ambiguous, architecture-changing, stakeholder-heavy, risky, or large enough that implementation should not begin before shared understanding is established.
---

# Align Project

Run epistemic alignment before implementation planning. The goal is not more documentation; it is a shared, inspectable model of the problem that exposes disagreement while it is still cheap to resolve.

## Contract

Input: absolute project root, human request, repository evidence, and any existing `alignment/` dossier.

Output: a concise process contract, then either a direct-work rationale or an initialized/resumed dossier and exactly one next skill.

Read [installed resources](../../references/installed-resources.md) and [the dossier contract](../../references/artifact-contract.md). Resolve bundled resources from this skill's installed path, never from the target project's working directory. Keep plugin root and project root separate.

## Calibrate before routing

Use the workflow when any of these is true:

- material ambiguity or competing interpretations;
- behavior crosses teams, systems, trust boundaries, or public interfaces;
- architecture, persistence, security, migration, or operations may change;
- multiple stakeholders carry different goals or failure costs;
- incorrect assumptions would cause expensive rework;
- the human explicitly requests alignment, use cases, BDD, C4, or stakeholder review.

Skip only genuinely bounded work whose expected behavior and affected surface are already clear. A small diff does not by itself make the problem bounded.

Before creating files, state a compact process contract:

- desired outcome and concrete deliverables;
- material risks and failure stakes that actually exist;
- reversibility and external effects;
- dossier phases and approval gates worth keeping;
- phases and gates intentionally omitted, with reasons;
- review binding: `conversational` by default or `exact-snapshot` when exact-byte provenance is materially required;
- recommended downstream rigor: `direct`, `bounded`, `full`, or `critical`.

Use `exact-snapshot` only when the human requests version-bound approval, a regulated/audited record needs it, asynchronous or multi-writer review creates a real stale-version risk, or downstream action is difficult to reverse. Do not introduce hashes merely because the helper supports them.

For direct work, report the contract in chat and create no dossier, approval state, or handoff. For aligned work, record the contract in `charter.md` and create only artifacts that resolve a named material question or risk. Cockburn, BDD, C4, semantic review, and a stakeholder Site are tools, not quotas.

## Process-dominance check

Before starting each phase or another review cycle, name the decision it will resolve or material risk it will reduce. If none exists, mark the phase `not needed` with a one-line reason and route onward. If two consecutive cycles add no new material information, or process work has overtaken the deliverable, stop and recalibrate the contract. Remove unsupported machinery instead of hardening it because it already exists.

## Start or resume

1. Resolve the bundled plugin root and absolute target root; resolve the helper only if using its initializer or exact-snapshot binding.
2. If aligned work needs a dossier and it is absent, run `"$ALIGNMENT_HELPER" init "$PROJECT_ROOT" --project-id <stable-id> --title <human title>`.
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

- material discovery uncertainty remains → `alignment:discover-domain`
- actor goals/interactions are material and Cockburn use cases are absent → `alignment:write-use-cases`
- behavior boundaries or guarantees are material and lack observable examples → `alignment:specify-behavior`
- responsibilities, interfaces, trust boundaries, or material choices need explanation → `alignment:model-architecture`
- cross-artifact review would expose a named coherence risk → `alignment:review-alignment`
- a stakeholder decision needs an inspectable presentation → `alignment:build-review`
- a current presentation awaits a human decision or handoff delivery → `alignment:approve-handoff`

Before transition, synchronize completed/skipped phases and `current_phase`. In `exact-snapshot` mode also synchronize `snapshot_paths`. Artifacts remain authoritative if phase metadata later drifts.

## Stop conditions

Stop when a missing human choice would materially alter the result, evidence is unavailable, or stakeholder authority is unclear. Report the blocker and affected artifacts. Do not turn alignment into implementation design, task decomposition, code generation, or a process-hardening project. The downstream process recommendation informs Superpowers but does not override its own risk calibration.

Final response: process contract, current phase, what is established, the most consequential uncertainty, files changed, and the one next skill.
