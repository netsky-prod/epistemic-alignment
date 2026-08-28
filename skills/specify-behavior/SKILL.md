---
name: specify-behavior
description: Use when priority use-case paths, extensions, rules, boundaries, or recovery outcomes need concrete observable examples before architecture and implementation planning.
---

# Specify Behavior

Turn goal models into examples stakeholders can challenge. BDD here is discovery and alignment: examples expose rules and boundary decisions; they are not merely test automation syntax.

## Contract

Input: discovery context, `alignment/use-cases/`, confirmed or explicitly proposed criteria, and existing feature files.

Output: linked `alignment/features/*.feature` files covering priority success, failure, boundary, and recovery behavior without prescribing internals.

Use [installed resources](../../references/installed-resources.md), the full [BDD method](../../references/bdd.md), and [dossier contract](../../references/artifact-contract.md).

## Build a behavior inventory

For each priority use case list:

- main success path and success guarantee;
- extensions that change a stakeholder-visible outcome;
- business rules with meaningful boundaries;
- assumptions that need examples to become discussable;
- contradictions that block one expected outcome;
- operational outcomes such as retry, duplicate suppression, recovery, notification, or audit.

Do not create one scenario per use-case step. Choose examples that distinguish one rule or outcome from another.

## Example discovery loop

For each behavior question:

1. name the use case, extension, or rule;
2. identify the smallest relevant starting context;
3. choose one concrete actor action or external event;
4. state the observable result, including important non-events;
5. probe the nearest boundary: inside/outside, missing, duplicate, late, unavailable, or conflicting;
6. ask one question if plausible answers change the stakeholder outcome;
7. mark inferred answers `proposed` rather than confirmed.

Prefer concrete examples over adjectives. Replace “large refund” with representative values or named policy categories when boundaries matter. If the number is unknown, record the missing rule instead of inventing it.

## Write readable Gherkin

Use one feature for a cohesive capability or rule set. Include:

- outcome-oriented feature title and narrative;
- `# alignment-meta` with source use case and status;
- stable `@SCN-###` and `@UC-###` tags;
- `Rule` blocks when examples illustrate one business rule;
- scenarios named by outcome;
- Given/When/Then steps in domain language.

Step discipline:

- `Given` establishes relevant observable context, not database setup;
- `When` expresses one business action or event;
- `Then` states an externally visible outcome or invariant;
- `And` stays at the same conceptual level;
- Background contains only truly common domain context;
- Scenario Outline is used only when examples illuminate a rule boundary.

Do not mention controllers, tables, queues, functions, mocks, or framework hooks unless stakeholders explicitly care about that protocol as behavior.

## Material scenario classes

Consider:

- representative success;
- business-rule rejection;
- minimum/maximum or before/after boundary;
- missing or invalid prerequisite;
- duplicate or repeated action;
- partial failure and recovery;
- dependency unavailable or delayed;
- cancellation or abandonment;
- authorization and privacy outcome;
- conflicting concurrent action;
- notification and audit outcome.

Include a class only when it changes a guarantee, stakeholder decision, architecture driver, or risk.

## Traceability and disagreement

Every scenario links to a use case or explains why it is cross-cutting. Link assumptions and open questions. When a scenario contradicts a use-case guarantee, record the mismatch and return to the responsible artifact/owner rather than quietly editing one side.

Use statuses:

- `confirmed` — supported by current authoritative evidence;
- `proposed` — useful interpretation awaiting confirmation;
- `conflicting` — sources imply different outcomes.

## Quality review

Read scenarios aloud as business examples. Confirm:

- stakeholders can understand them without code knowledge;
- each scenario demonstrates a meaningful distinction;
- Then clauses are observable and specific;
- main guarantees and material extensions have examples;
- boundaries reveal decisions instead of combinatorial noise;
- proposed behavior is visible;
- architecture has not leaked into acceptance language;
- IDs and source links are stable.

When examples expose the architecture-driving responsibilities, add `behavior` to `completed_phases` and set `current_phase` to the next material phase. Synchronize feature paths in `snapshot_paths` only in exact-snapshot mode.

Next transition: `alignment:model-architecture`.
