Feature: Export lifecycle under conflicting requirements
  The Finance and Support statements are both current, so the policy remains
  unresolved until the COO decides.

  # Evidence: STMT-FIN-001, STMT-SUP-001, CON-001, OWNER-COO-001
  Scenario: Preserve both current requirements for review
    Given Finance requires irreversible exports
    And Support requires a cancellation window
    When the export lifecycle is reviewed
    Then both requirements remain visible
    And the conflict is marked unresolved

  Scenario: Defer implementation behavior while the conflict is open
    Given the COO is the future decision owner
    And no resolution has been supplied
    When an export policy is requested
    Then no side is selected
    And no implementation authorization is inferred
