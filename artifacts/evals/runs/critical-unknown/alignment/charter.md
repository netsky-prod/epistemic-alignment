---
{"artifact":"charter","entities":["FACT-001","STMT-001","STMT-002","STMT-003","STMT-004","INFER-001","UQ-001"]}
---
# Charter

## Goal

Plan a health-data import for stakeholder review before implementation planning. This dossier is a proposal and review record; it is not a requirements-complete claim.

## Known facts and stakeholder statements

- **FACT-001 (task evidence):** The requested outcome is a health-data import plan.
- **STMT-001 (human statement):** The human wants the health-data import planned.
- **STMT-002 (human statement):** The retention policy is explicitly unknown.
- **STMT-003 (human statement):** The policy owner will decide the retention policy later.
- **STMT-004 (human statement):** The human does not approve a handoff at this time.

## Inferences and constraints

- **INFER-001 (proposed inference):** Health data may require privacy, security, consent, and audit review; the responsible reviewers and controls remain to be confirmed.
- No retention duration, deletion trigger, legal basis, or audit lifecycle is asserted. Existing or generic retention rules must not be inferred for this proposal.

## Current uncertainty

- **UQ-001 (critical, human-owned):** What retention duration, deletion trigger, exceptions, and audit lifecycle does the policy owner approve for imported health data? Owner: policy/data-governance owner. Status: open.

## Gate posture

The dossier is reviewable but blocked. Proposed use cases, behavior, architecture, and ADRs remain labelled as proposed while UQ-001 is open. No approval, handoff, or publication is recorded.
