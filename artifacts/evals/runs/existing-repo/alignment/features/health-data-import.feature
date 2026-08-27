# alignment-meta: {"use_case":"UC-001","status":"proposed","source":"existing-repo scripted human answer"}
@SCN-001 @UC-001
Feature: Import health data with policy-bound storage
  Rule: Health-data records are stored only when validation, authorization, and retention policy are confirmed.

  Scenario: Authorized actor imports valid health data under a confirmed policy
    Given an authorized actor has an in-scope health-data source
    And the source format and retention policy are confirmed
    When the actor confirms the validated import
    Then the system stores the valid records under the confirmed retention policy
    And the system reports the import result

  @SCN-002
  Scenario: Retention policy is unresolved
    Given an authorized actor has a valid health-data source
    And the retention policy is unresolved
    When the actor requests the import
    Then the system does not durably store health-data records
    And the system reports that a policy decision is required

  @SCN-003
  Scenario: Invalid source is recoverable
    Given an authorized actor has a source with unsupported or invalid records
    When the actor requests validation
    Then the system identifies the rejected input
    And the system reports a recoverable validation outcome without claiming import success
