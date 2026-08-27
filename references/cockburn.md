# Cockburn use-case method

Use cases model actor goals and the system's behavioral responsibilities. They sit between discovery and examples: more structured than a stakeholder story, less concrete than BDD.

## Goal levels

- **Summary:** groups several user goals into a larger business process.
- **User goal:** one meaningful result a primary actor seeks in a sitting or business event.
- **Subfunction:** reused or independently risky behavior that supports user goals.

Default to user-goal level. A title such as “Manage refunds” is probably summary-level; “Receive an eligible refund” is a user goal; “Verify refund eligibility” may be a subfunction.

## Full template

```markdown
# UC-<id>: <verb and stakeholder outcome>

Status: proposed | confirmed | conflicting
Scope: <software system or business area>
Level: summary | user-goal | subfunction
Primary actor: <role whose intent drives the case>
Supporting actors/systems: <only responsibility exchanges>

## Goal and source
<desired outcome; link discovery goal/evidence>

## Stakeholder interests
- <stakeholder>: <value sought, risk avoided, or obligation>

## Conditions and guarantees
- Preconditions: <what must already be true>
- Minimal guarantee: <protected outcome on failure>
- Success guarantee: <observable result on success>
- Trigger: <intent or external event>

## Main success scenario
1. <actor intent or action>
2. <system responsibility / observable response>
3. ...

## Extensions
- 2a. <condition>: <response, recovery/termination, and return point>
- 3a. <condition>: ...

## Business rules and constraints
- <rule ID, statement, source, status>

## Frequency / volume
<evidence-backed estimate or unknown>

## Traceability
- Goals:
- Assumptions / contradictions:
- Open questions:
- Scenarios: pending

## Open issues
- <issue and owner>
```

## Writing main steps

Each step expresses actor intent or system responsibility at roughly the same altitude. A step should be independently understandable and advance the goal. Avoid UI choreography, internal component names, and passive phrases such as “data is processed.”

Useful sequence:

1. actor initiates with an intent;
2. system obtains or validates information relevant to the goal;
3. actor supplies a choice only they can make;
4. system fulfills a responsibility or refuses under a rule;
5. system communicates the outcome and preserves guarantees.

## Discovering extensions

For every step probe:

- invalid/missing information;
- business-rule boundary;
- authorization or privacy failure;
- duplicate, stale, or concurrent action;
- dependency unavailable or delayed;
- partial completion;
- actor cancellation;
- alternative success route;
- recovery and notification.

An extension names the condition and outcome, then says whether the case resumes at a step, succeeds differently, or terminates under the minimal guarantee.

## Common failure modes

- **Feature list:** no actor goal or guarantees.
- **Screenplay:** every click is a step, while intent is invisible.
- **Happy-path only:** no recovery or minimal guarantee.
- **Architecture leakage:** controllers, tables, queues, or services define behavior prematurely.
- **Vague guarantees:** “request processed successfully.”
- **False certainty:** missing policy is filled with a plausible rule.
- **Actor confusion:** the named primary actor does not own the triggering intent.

## Review questions

- Would the primary actor recognize this as their goal?
- Does the success guarantee follow from the main scenario?
- Does every extension preserve the minimal guarantee?
- Are important stakeholder interests reflected in steps, rules, or guarantees?
- Can BDD examples be derived without inventing policy?
- Would the use case survive a major interface redesign?
