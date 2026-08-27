---
name: approve-handoff
description: Use when a stakeholder has inspected an issued alignment presentation, may provide a current decision, or an already verified handoff is awaiting delivery into Superpowers.
---

# Approve Handoff

Convert a current human decision into a mechanically bound handoff without making the human operate the hash protocol. Approval means “this dossier is an adequate basis for downstream brainstorming,” not “the implementation is correct” or “all uncertainty is gone.”

## Contract

Input: absolute project root; issued presentation; current dossier/review state; visible findings; either a current human reply or an existing verified handoff awaiting delivery.

Output: `changes_requested`, `rejected`, a verified `alignment/handoff.md`, or a verified handoff whose delivery is explicitly pending.

Use [installed resources](../../references/installed-resources.md) and [thin approval](../../references/approval.md). All helper commands use the resolved absolute `$ALIGNMENT_HELPER`; never assume `scripts/alignment` exists in the target project.

## Resume before asking again

If `alignment/handoff.md` already exists, do not restart approval automatically.

1. Run `"$ALIGNMENT_HELPER" check "$PROJECT_ROOT" --json`.
2. If not ready, do not deliver the old handoff. Explain which source/state changed and return to presentation/reapproval.
3. If ready and Superpowers is unavailable, preserve all bytes and state; report `delivery pending` with the exact handoff path.
4. If ready and Superpowers is available, read the handoff and all dossier paths it names, then run the check again. Only an unchanged final check may enter `superpowers:brainstorming`.
5. Never ask for another decision, rerun `decide`, or regenerate handoff merely because delivery was delayed.

## Prepare the decision request

Before asking the human:

1. Read `review-state.json`, `review.md`, presentation location, and current snapshot.
2. Confirm the presentation is the issued view of the same current snapshot.
3. Confirm every reviewable artifact is in `snapshot_paths`.
4. Summarize open/material findings, accepted limitations, and what approval unlocks.
5. Make clear that approval does not certify semantics, security, estimates, or implementation details.

Ask one direct question:

> Do you approve this reviewed dossier as the basis for downstream brainstorming, request changes, or reject it?

Accept natural explicit replies equivalent to `approved`, `changes_requested`, or `rejected`. The human does not need to repeat a digest, reviewer label, CLI flag, or finding ID.

## Authority rules

A valid decision must be:

- from a human in the current interaction;
- explicit rather than inferred;
- about the currently presented dossier;
- made after the stakeholder had access to the presentation and findings.

Invalid authority includes silence, “looks interesting,” generic earlier permission, approval of the plugin design rather than this dossier, a Site button, agent confidence, edited state, a test fixture, or replay of a historical decision after a new issuance.

If the reply is ambiguous, ask a short clarification. Never steer the person toward approval.

## Bind the human reply internally

The agent—not the human—reads the issued digest and translates the decision to the helper:

```sh
"$ALIGNMENT_HELPER" decide "$PROJECT_ROOT" \
  --decision <approved|changes_requested|rejected> \
  --reviewer "<honest human label>" \
  --provenance human-message \
  --review-hash <current-issued-digest> \
  --acknowledged-finding <ID>
```

Repeat `--acknowledged-finding` for each finding the human explicitly accepts. Do not acknowledge findings on their behalf. Bind only to the existing issued digest; do not issue a new review after receiving the reply and then reuse the old reply.

## Outcomes

### Changes requested

Record the decision, summarize requested changes in canonical artifacts, identify the earliest affected phase, and route there. Any later presentation requires a new issuance and new decision. Produce no handoff.

### Rejected

Record closure and the stated reason when supplied. Do not generate handoff or treat rejection as a request for autonomous redesign.

### Approved

Run:

```sh
"$ALIGNMENT_HELPER" check "$PROJECT_ROOT" --json
"$ALIGNMENT_HELPER" handoff "$PROJECT_ROOT"
"$ALIGNMENT_HELPER" check "$PROJECT_ROOT" --json
```

Continue only when the gate reports ready and the generated handoff is verified for the unchanged dossier. Never create, repair, or edit approval hashes or handoff metadata manually.

## Delivery into Superpowers

The downstream consumer must read:

- `alignment/handoff.md`;
- manifest and every included dossier path;
- `alignment/review.md` and acknowledged findings;
- stated assumptions, contradictions, and open questions.

Then recheck the gate immediately before doing downstream creative work. If stale, consume nothing as approved authority and return to presentation/reapproval.

Invoke `superpowers:brainstorming` with the dossier as required context. The handoff constrains and informs brainstorming; it does not skip Superpowers' own design conversation or authorize implementation.

Add `approval` to `completed_phases` only through canonical artifact updates that do not alter the approved snapshot after decision. Final response names the human outcome, handoff/delivery status, exact next skill, and any accepted limitation—without asking the human to handle hashes.
