# alignment-meta: {"use_case":"UC-001","status":"proposed"}
@SCN-001 @UC-001
Feature: Reviewable billing handoff
  Rule: Billing authority and uncertain rules stay visible until a responsible human decides.

  Scenario: Present a bounded handoff for human review
    Given the sponsor is recorded as the product owner
    And the billing owner and authoritative billing rules are unresolved
    When the alignment dossier is presented for review
    Then the review surface shows the goal, evidence references, open findings, and snapshot digest
    And it labels billing ownership and rule criteria as unresolved or proposed
    And it states that no decision has been recorded

  @boundary
  Scenario: Missing billing owner prevents handoff approval
    Given no billing owner has been named
    And no explicit human decision message is supplied for the presented snapshot
    When the handoff gate is evaluated
    Then the gate reports that handoff is blocked
    And the dossier retains `Q-001` and `Q-003` as open questions
