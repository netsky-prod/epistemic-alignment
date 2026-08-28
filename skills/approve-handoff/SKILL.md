---
name: approve-handoff
description: Use when a stakeholder has inspected an alignment presentation, may provide a current decision, or an approved handoff is awaiting delivery into Superpowers.
---

# Approve Handoff

Convert a current human decision into a transparent handoff. Approval means “this dossier is an adequate basis for downstream brainstorming,” not “the implementation is correct” or “all uncertainty is gone.”

## Contract

Input: absolute project root; current presentation and dossier; visible findings; process contract; either a current human reply or an existing handoff awaiting delivery.

Output: `changes_requested`, `rejected`, or `alignment/handoff.md` with an explicit binding mode and downstream-rigor recommendation.

Use [installed resources](../../references/installed-resources.md) and [human decision and handoff](../../references/approval.md). Resolve the helper only when the process contract selected `exact-snapshot`.

## Recalibrate before the decision

Read the process contract. Confirm that every retained gate still protects a named material risk or decision. If exact-snapshot binding was selected but its justification no longer exists, propose conversational binding and let the human override. Never silently strengthen the gate because tooling is available or prior work has already been spent on it.

Approval itself remains human-owned whenever a stakeholder decision is the purpose of the review. Recalibration can remove mechanical ceremony; it cannot manufacture consent.

## Resume before asking again

If `alignment/handoff.md` already exists, do not restart approval automatically.

1. Read the handoff, current dossier, presentation reference, and binding mode.
2. In conversational mode, compare the current material claims/findings to those named in the handoff. If materially changed, do not deliver it; return to presentation.
3. In exact-snapshot mode, run `"$ALIGNMENT_HELPER" check "$PROJECT_ROOT" --json`; only `ready: true` may continue.
4. If Superpowers is unavailable, preserve the handoff and report `delivery pending` with its exact path.
5. Never ask for another decision merely because delivery was delayed.

## Prepare the decision request

Show the stakeholder:

- presentation location;
- open/material findings and accepted limitations;
- remaining assumptions, contradictions, and questions;
- what approval unlocks and what it does not certify;
- conversational or exact-snapshot binding, with its rationale;
- recommended downstream rigor, retained gates, and intentionally omitted gates.

Ask one direct question:

> Do you approve this reviewed dossier as the basis for downstream brainstorming, request changes, or reject it?

Accept natural explicit replies equivalent to `approved`, `changes_requested`, or `rejected`. The human never needs to repeat a digest, reviewer label, CLI flag, or finding ID.

## Authority rules

A valid decision is explicit, from a human in the current interaction, about the currently presented dossier, after access to the presentation and findings.

Silence, generic earlier permission, approval of the plugin design, a Site button, agent confidence, edited state, a test fixture, or a replayed historical decision is not authority. If the reply is ambiguous, ask one short clarification. Never steer the person toward approval.

## Outcomes

### Changes requested

Record the requested changes, identify the earliest materially affected phase, update the process contract if scope/risk changed, and route there. A materially changed presentation needs a new current decision. Produce no handoff.

### Rejected

Record closure and the stated reason when supplied. Do not create a handoff or treat rejection as permission for autonomous redesign.

### Approved — conversational binding

Write `alignment/handoff.md` for humans. Include:

- decision and descriptive reviewer label;
- provenance: current human message;
- presentation reference and reviewed source paths;
- accepted findings and remaining uncertainty;
- explicit statement: `not exact-byte bound`;
- recommended downstream rigor;
- gates retained, gates omitted, and escalation/downgrade triggers.

Read the named dossier sources again before delivery. If a material claim or finding changed, return to presentation and request a current decision. Do not pretend this comparison is cryptographic proof.

### Approved — exact-snapshot binding

Bind the existing issued digest internally; the human does not copy it:

```sh
"$ALIGNMENT_HELPER" decide "$PROJECT_ROOT" \
  --decision approved \
  --reviewer "<honest human label>" \
  --provenance human-message \
  --review-hash <current-issued-digest> \
  --acknowledged-finding <ID>

"$ALIGNMENT_HELPER" check "$PROJECT_ROOT" --json
"$ALIGNMENT_HELPER" handoff "$PROJECT_ROOT"
"$ALIGNMENT_HELPER" check "$PROJECT_ROOT" --json
```

Repeat `--acknowledged-finding` only for findings the human explicitly accepts. Never issue a new review and bind the old reply to it; never edit hashes or handoff metadata manually.

## Delivery into Superpowers

The downstream consumer reads `handoff.md`, the process contract, canonical dossier sources it names, `review.md`, and accepted limitations. Exact-snapshot mode also requires one final successful helper check.

Invoke `superpowers:brainstorming` with this material as context. The downstream-rigor recommendation is evidence, not command: Superpowers must recalibrate against current risk and may move in either direction. Preserve hard gates for irreversible, destructive, security-sensitive, or external actions; do not automatically add planning, TDD, review fanout, or release ceremony when the recommended rigor and actual risks do not justify them.

Final response names the human outcome, binding mode, handoff/delivery status, downstream-rigor recommendation, and accepted limitations—without asking the human to operate the hash protocol.
