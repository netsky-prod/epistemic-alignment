---
{"artifact":"charter","entities":["GOAL-001","STMT-FIN-001","STMT-SUP-001","OWNER-COO-001","CON-001","UQ-001"]}
---
# Charter

## Goal

Align the export workflow with Finance and Support before implementation. The
human confirmed both stakeholder requirements are current, deferred resolution,
and named the COO as the future decision owner. No approval was given.

## Evidence boundary

- `STMT-FIN-001` — Finance requires exports to be irreversible.
- `STMT-SUP-001` — Support requires a cancellation window for exports.
- `OWNER-COO-001` — The COO is the named future owner for resolving the conflict.
- `CON-001` — The two current requirements conflict for the same export flow.

## Constraints and uncertainty

- Both statements remain current and must remain visible; neither is discarded.
- `UQ-001` (critical): Which export policy should govern, and what exact
  cancellation/irreversibility semantics should implementation use?
- Resolution is deferred to `OWNER-COO-001`; no decision or implementation
  authorization is recorded.

## Current phase

Discovery, semantic review, and a read-only derived review payload are drafted.
The gate is blocked because `CON-001` remains unresolved and no current explicit
approval exists.
