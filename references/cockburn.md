# Cockburn use-case recipe

Create one file per material user goal: `use-cases/UC-<id>.md`.

```markdown
# UC-<id>: <verb and outcome>

Scope: <system>
Level: <summary|user-goal|subfunction>
Primary actor: <actor>

Stakeholder interests:
- <stakeholder>: <interest>

Preconditions: <state>
Minimal guarantee: <what remains true on failure>
Success guarantee: <observable outcome>
Trigger: <event>

## Main success scenario
1. <actor intent>
2. <system responsibility>

## Extensions
- 2a. <condition>: <response and recovery>

Business rules: <rules or links>
Frequency: <estimate or unknown>
Open issues: <IDs or none>
```

Model intent, responsibilities, guarantees, and recovery. Describe UI clicks only where interface behavior is contractual.
