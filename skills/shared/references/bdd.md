# BDD example recipe

Write `features/<area>.feature` for priority use cases and material extensions. A scenario is an observable example, not an implementation sketch.

```gherkin
# alignment-meta: {"use_case":"UC-001","status":"proposed"}
@SCN-001 @UC-001
Feature: <outcome>
  Rule: <business rule>

  Scenario: <observable result>
    Given <relevant starting context>
    When <actor action or event>
    Then <visible outcome>
    And <invariant or notification>
```

Use examples to make main flows, failure paths, boundaries, and decisions reviewable. Clearly label proposed criteria until a human confirms them.
