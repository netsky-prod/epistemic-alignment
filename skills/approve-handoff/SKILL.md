---
name: approve-handoff
description: Use when a stakeholder has reviewed an issued alignment presentation and may provide a current explicit decision on the exact snapshot.
---

# Approve Handoff

Record an explicit human decision for the snapshot the stakeholder actually reviewed.

## Contract

Input: either an existing `alignment/handoff.md` awaiting delivery, or a presented review reference, `alignment/review.md`, issued snapshot state, and a current human message. Output: either a recorded non-approval outcome, verified `alignment/handoff.md`, or that verified handoff with delivery pending. Read [thin approval](../../references/approval.md).

## Pending Delivery Resume

Before normal approval, if `alignment/handoff.md` exists, run the read-only `scripts/alignment check <root> --json` as a mandatory fresh-context check.

- When the check returns `ready: true`, the existing handoff is verified for the current dossier. Do not ask for a decision, do not run `scripts/alignment decide`, and do not run `scripts/alignment handoff` or regenerate the handoff. If `superpowers:brainstorming` is available, deliver the existing handoff and dossier to it. If `superpowers:brainstorming` is unavailable, leave the verified `alignment/handoff.md` and approval state untouched. Report delivery pending with the exact `alignment/handoff.md` path, and resume the transition when `superpowers:brainstorming` becomes available.
- When the check is not ready or cannot verify freshness, do not deliver. Return to presentation and reapproval with the normal existing mechanics; the old handoff is not authority for the changed dossier.

## Normal Approval

1. Inspect `review-state.json`, `review.md`, presentation location, and `scripts/alignment snapshot <root> --json`. Verify every current reviewable dossier file is listed in manifest `snapshot_paths` before issue-review; restart at presentation if membership or the current snapshot differs from the issued hash.
2. Show the human the Site or other review reference, `review.md` findings and dispositions, and the current snapshot hash. Ask one direct question for `approved`, `changes_requested`, or `rejected`. The human does not need to repeat or copy the digest in the reply.
3. Accept approval only from an explicit human message in the current interaction. The agent binds that reply internally to the current issued digest, then runs `scripts/alignment decide <root> --decision approved --reviewer <label> --provenance human-message --review-hash <hash> --acknowledged-finding ID [--acknowledged-finding ID ...]`; use the same command with the current decision value for other outcomes. Never bind a reply to a superseded issuance or infer a decision from an ambiguous message.
4. For `changes_requested`, return to the relevant authoring skill; for `rejected`, report closure without handoff. For `approved`, run `scripts/alignment check <root> --json`, then `scripts/alignment handoff <root>` only when ready.
5. After the handoff is verified, transition with it and the dossier only if `superpowers:brainstorming` is available. If `superpowers:brainstorming` is unavailable, use the same delivery-pending reporting and preservation behavior above. Do not regenerate the handoff or mutate approval state merely because delivery is pending.

Agents must never self-approve: silence, generic prior permission, a Site button, agent confidence, and a pre-edited state file are not an explicit human message. The current snapshot must remain unchanged. Next transition when available: `superpowers:brainstorming` with `handoff.md` and the dossier.
