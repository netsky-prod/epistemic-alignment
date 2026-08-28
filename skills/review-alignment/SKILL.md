---
name: review-alignment
description: Use when a dossier needs an independent semantic cross-review of goals, stakeholders, use cases, examples, architecture, decisions, evidence, and unresolved uncertainty before presentation.
---

# Review Alignment

Read the dossier as a skeptical independent reviewer. The purpose is to expose mismatches and hidden uncertainty for human judgment, not to certify correctness.

## Contract

Input: complete current dossier and relevant repository/supplied evidence.

Output: `alignment/review.md` with review scope, evidence-backed findings, impact, ownership, and explicit disposition.

Use [installed resources](../../references/installed-resources.md), the full [semantic review method](../../references/semantic-review.md), and [dossier contract](../../references/artifact-contract.md).

## Establish review scope

Record:

- binding mode and dossier version/source set being reviewed;
- files and evidence actually inspected;
- important sources unavailable to the reviewer;
- stakeholder perspectives represented or missing;
- limits of the review.

Read source artifacts afresh. Do not rely on the authoring conversation's summary.

## Review passes

### 1. Goal and stakeholder pass

Check whether desired outcomes, non-goals, scope, and constraints are clear. Look for outcomes with no stakeholder, stakeholders with no represented interest, and missing decision authority.

### 2. Epistemic pass

Look for inference written as fact, assumption without impact/validation path, silently resolved contradiction, closed question without evidence, weak provenance, and terms whose meaning changes across files.

### 3. Use-case pass

Check whether priority goals have a primary actor, observable guarantees, a coherent main path, material extensions, and recovery. Look for screen flows masquerading as goals and failure cases that violate the minimal guarantee.

### 4. Behavior pass

Map guarantees, extensions, and business rules to scenarios. Look for important paths without examples, examples without a source goal, vague outcomes, missing boundaries, implementation leakage, and proposed behavior presented as confirmed.

### 5. Architecture pass

Walk priority scenarios through context/containers/components. Look for unowned responsibilities, unexplained external dependencies, invisible trust/data boundaries, missing recovery ownership, diagrams that disagree with prose, and depth without decision value.

### 6. Decision pass

Check whether material choices have owners, drivers, alternatives, consequences, risks, and invalidating assumptions. Identify accidental choices embedded only in diagrams or examples.

### 7. Stakeholder-readiness pass

Ask whether a non-author stakeholder can understand what is proposed, what is known, what remains uncertain, which findings require acceptance, and what exactly approval would authorize.

Check the process contract too: every retained phase/gate should protect a named risk or decision; every omission should remain safe; binding mode and downstream rigor should match reversibility and failure stakes. Treat unsupported process machinery as scope to remove, not architecture to harden.

## Traceability walk

Select each critical outcome and follow it end to end:

`stakeholder → goal → use case → scenario → responsibility → ADR/finding`

Then walk backward from every material container/component/ADR to the behavior and goal that justify it. Missing links become findings; they are not automatically defects if the dossier explicitly explains why the artifact is cross-cutting.

## Finding format

Every finding includes:

- stable `FINDING-###` ID;
- concise statement of the mismatch or uncertainty;
- concrete evidence paths/IDs;
- stakeholder or implementation impact;
- severity: blocking, material, or advisory;
- suggested owner and next action;
- disposition: open, accepted limitation, resolved, or superseded;
- acknowledgment requirement when approval may proceed despite it.

Do not use severity to simulate mathematical certainty. “Blocking” means the reviewer believes meaningful stakeholder approval is not possible until resolved.

## Reviewer behavior

Ask one material question only when evidence cannot locate or characterize a finding. When an answer changes a source artifact, update that artifact and rerun affected review passes. Do not repair substantive issues only in `review.md`.

Before transition confirm that open blocking findings are clearly visible, accepted limitations name their consequences, resolved findings link to changed evidence, and review scope remains honest.

Add `review` to `completed_phases` and set `current_phase` to `presentation`. In exact-snapshot mode, include `review.md` and all current reviewable artifacts in `snapshot_paths`. Leave semantic judgment to the human stakeholder.

Next transition: `alignment:build-review`.
