# alignment-meta: {"use_case":"UC-101","status":"proposed"}
@UC-101
Feature: Receive an observable expedited refund outcome
  Rule: Each purchase has one stable accepted refund request

    @SCN-101 @confirmed
    Scenario: Eligible customer receives an acceptance receipt
      Given an eligible customer has a purchase with a stable purchase reference
      When the customer submits an expedited refund request for that purchase
      Then the request is accepted
      And the customer receives a receipt containing a stable refund request ID

    @SCN-102 @confirmed
    Scenario: Repeating an accepted request returns the original outcome
      Given an expedited refund request for a purchase was already accepted
      And the customer received its acceptance receipt
      When the customer repeats the same expedited refund request
      Then the customer receives the same acceptance receipt with the same refund request ID
      And no second refund is created

    @SCN-103 @proposed @ASM-102
    Scenario: Ineligible request offers a review path
      Given a customer is known to be ineligible for an expedited refund
      When the customer submits an expedited refund request for the purchase
      Then the request is not accepted
      And the customer receives the policy reason
      And the customer is offered a human-review path
