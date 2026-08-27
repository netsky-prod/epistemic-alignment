# alignment-meta: {"use_case":"UC-001","status":"proposed"}
@SCN-001 @UC-001
Feature: Import health data under a confirmed policy
  Rule: Imported health data is retained and deleted only according to a confirmed policy

  # Proposed acceptance criteria; no human confirmation has been recorded.
  Scenario: Authorized valid import under confirmed retention policy
    Given an authorized health-data source passes the agreed validation rules
    And the policy/data-governance owner has supplied a confirmed retention policy
    When the product stakeholder requests the import
    Then the system imports the valid records
    And the stored records expose their policy-linked retention and audit reference

  # Proposed boundary example; UQ-001 is intentionally human-owned.
  @SCN-002
  Scenario: Import pauses when retention policy is unknown
    Given an otherwise valid and authorized health-data source
    And the retention policy is explicitly unknown (UQ-001)
    When the product stakeholder requests the import
    Then the system does not claim durable retention or deletion behavior
    And the system identifies the policy/data-governance owner and pauses for that decision
    And no handoff or approval is implied by the paused state

  @SCN-003
  Scenario: Invalid source is recoverable
    Given a health-data source fails an agreed validation rule
    When the product stakeholder requests the import
    Then the system rejects the invalid input with an actionable explanation
    And existing imported data remains unchanged
