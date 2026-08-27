@UC-001
Feature: Release only an unchanged human-approved alignment handoff
  The delivery team needs the exact reviewed context to reach Superpowers planning.

  @SCN-001
  Scenario: Explicit approval of the unchanged presented snapshot
    Given a local review Site displays the current dossier digest
    And the semantic findings are visible to the release sponsor
    When the release sponsor explicitly approves that exact digest
    And the included dossier files remain unchanged
    Then the mechanical gate is ready
    And the handoff carries the same digest
    And Superpowers brainstorming receives the dossier as required context

  @SCN-002
  Scenario: Included content changes after approval
    Given the release sponsor approved the issued digest
    When an included dossier file changes
    Then the gate reports stale approval
    And no handoff is created for the changed content

  @SCN-003
  Scenario: Agent confidence is not approval
    Given the Site and semantic review appear complete to the agent
    When no current human approval message exists
    Then the decision remains unapproved
    And no handoff is created
