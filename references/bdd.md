# BDD example-discovery method

BDD examples turn rules, guarantees, and extensions into concrete conversations. Gherkin is the durable notation; the reasoning happens before syntax.

## Three-example probe

For a material rule, begin with:

1. a representative example that should succeed;
2. the nearest example that should not succeed or should produce a different outcome;
3. an ambiguous example that exposes missing policy.

Ask which facts explain the different outcomes. Those facts become domain context and rules—not implementation setup.

## Feature structure

```gherkin
# alignment-meta: {"use_case":"UC-001","status":"proposed","evidence":["alignment/use-cases/UC-001.md"]}
@UC-001
Feature: <stakeholder outcome>
  In order to <value>
  As a <role>
  I need <capability/outcome>

  Rule: <business rule in domain language>

    @SCN-001
    Scenario: <observable outcome under a meaningful condition>
      Given <smallest relevant domain context>
      When <one actor action or event>
      Then <observable result>
      And <important invariant, message, or non-event>
```

## Step semantics

- **Given:** facts relevant to the rule, already true before the action.
- **When:** one business action or event under discussion.
- **Then:** state or information observable outside implementation internals.
- **And/But:** facts at the same conceptual level as the preceding keyword.

Use domain nouns and verbs from the glossary. Avoid imperatives such as “call endpoint,” “insert row,” “mock service,” or “wait 500 ms” unless that protocol/timing is itself a stakeholder contract.

## Choosing scenario coverage

Prioritize examples that change:

- success or minimal guarantee;
- stakeholder-visible response;
- rule interpretation;
- authorization/privacy outcome;
- recovery behavior;
- architecture-driving quality or integration behavior.

Probe values just below/at/above a boundary; absent versus present; first versus duplicate; ordered versus out-of-order; available versus unavailable; authorized versus unauthorized; single versus conflicting concurrent action.

Do not enumerate a Cartesian product. When examples have the same reasoning and outcome, choose representative cases.

## Scenario Outline

Use an outline when a table of examples teaches one rule:

```gherkin
Scenario Outline: Refund eligibility follows the merchant window
  Given an order completed <age> days ago
  When the buyer requests a refund
  Then the request is <outcome>

Examples:
  | age | outcome  |
  | 13  | accepted |
  | 14  | accepted |
  | 15  | declined |
```

If the boundary value is not authoritative, label the rule and scenario proposed and retain the policy question.

## Status and traceability

Every feature/scenario links to a use case, rule, finding, assumption, or explicit cross-cutting concern. Preserve:

- `confirmed` for current authoritative evidence;
- `proposed` for a concrete interpretation awaiting agreement;
- `conflicting` when sources predict different outcomes;
- `obsolete` only with a replacement/source explanation.

## Anti-patterns

- one scenario per use-case step;
- scenarios that restate examples without a rule distinction;
- multiple When actions obscuring which event is evaluated;
- Then clauses about internal calls rather than outcomes;
- hidden global Background that makes examples unreadable;
- invented values presented as policy;
- brittle UI wording when the contract is the underlying outcome;
- “edge cases” selected mechanically rather than by stakeholder consequence.

## Review questions

- Can a stakeholder explain why the example should produce that outcome?
- Does it clarify a guarantee, extension, rule, or risk?
- Is the starting context minimal but sufficient?
- Is the Then observable and falsifiable?
- Are proposed decisions visibly proposed?
- Does a contradictory example trigger artifact review rather than silent reconciliation?
