---
name: write-use-cases
description: Use when discovered stakeholder goals and constraints need Cockburn-style goal models with guarantees, responsibilities, extensions, and unresolved issues before examples or architecture are designed.
---

# Write Use Cases

Describe what actors are trying to accomplish and what the system must guarantee. A use case is a goal contract, not a screen flow, API design, or backlog ticket.

## Contract

Input: discovery dossier, stakeholder goals, domain vocabulary, constraints, assumptions, contradictions, and existing use cases.

Output: reviewable `alignment/use-cases/UC-*.md` files linked to discovery evidence and suitable for deriving BDD examples.

Use [installed resources](../../references/installed-resources.md), the full [Cockburn method](../../references/cockburn.md), and [dossier contract](../../references/artifact-contract.md).

## Choose the right goal

Start from a stakeholder outcome, not a feature noun. A user-goal use case:

- begins when an actor forms an intent or an external event occurs;
- ends with a recognizable result or a minimal guarantee after failure;
- has enough independent meaning to discuss success and failure;
- remains meaningful if the interface changes.

Split when primary actor, trigger, success guarantee, or lifecycle differs. Combine steps that merely describe internal sequencing. Use summary cases to organize several user goals; use subfunctions only when shared behavior is materially reusable or risky.

## Authoring sequence

### 1. Identity and scope

Choose a stable `UC-###` ID and verb–outcome title. State system scope and level: summary, user-goal, or subfunction.

### 2. Actors and interests

Name the primary actor whose intent drives the case. Add supporting actors only when they exchange responsibility. Capture interests that constrain success: privacy, safety, money, audit, operations, support, and recovery.

### 3. Execution contract

Write:

- preconditions — what must already be true but is not established here;
- trigger — the event that starts the case;
- minimal guarantee — what remains protected on failure;
- success guarantee — observable state after success.

Do not hide behavior inside preconditions. Make guarantees specific enough to challenge.

### 4. Main success scenario

Use numbered steps alternating actor intent and externally meaningful system responsibility. Each step advances the goal, validates a business condition, or communicates a result. Keep technology out unless the protocol itself is contractual.

Prefer “The system verifies the refund remains within the permitted window” over “The controller calls RefundService.validate().”

### 5. Extensions and recovery

For every main step ask:

- what can prevent completion?
- what actor choice changes the outcome?
- what rule creates a boundary?
- what happens after duplicate action, timeout, unavailable dependency, partial completion, or cancellation?
- how does the actor learn what happened and recover?

Write `<step><letter>. <condition>: <response, outcome, and return or termination point>`. Preserve unknown policy as an issue instead of guessing.

### 6. Rules and uncertainty

Reference constraints, glossary terms, assumptions, contradictions, policies, and questions by readable ID/path. Mark unconfirmed rules `proposed`. When stakeholders require incompatible guarantees, stop for authority rather than silently choosing.

## Traceability

For each case keep a human-readable map of:

- discovery goals served;
- stakeholders affected;
- main path and material extensions;
- business rules;
- assumptions and open questions;
- BDD scenario IDs once created.

This is navigation, not machine certification.

## Quality review

Read each case from the perspectives of primary actor, operator, and failure-affected stakeholder. Confirm:

- title expresses a goal, not a UI action;
- primary actor owns the intent;
- guarantees are observable and non-circular;
- main scenario reaches the success guarantee;
- extensions attach to concrete steps and explain recovery or termination;
- stakeholder interests appear in guarantees, rules, or extensions;
- ambiguous policy remains visible;
- steps do not dictate architecture prematurely.

Ask one material question when intent, guarantee, or conflict is unclear, and update discovery before revising the case.

When priority user goals and material extensions are reviewable, add `use-cases` to `completed_phases`, set `current_phase` to `behavior`, and synchronize all use-case paths in `snapshot_paths`.

Next transition: `alignment:specify-behavior`.
