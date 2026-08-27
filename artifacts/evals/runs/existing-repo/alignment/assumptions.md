---
{"artifact":"assumptions","entities":[]}
---
# Assumptions
# Assumptions

- `ASM-001` (explicit, medium): The existing importer and storage path are relevant starting points for the proposed flow. Source: `FACT-001`–`FACT-003`; validate during technical discovery.
- `ASM-002` (explicit, low): A health-data import may require stricter handling than the current generic 30-day retention. Source: `INFER-001`; policy owner must decide.
- `ASM-003` (explicit, low): A source adapter can normalize an approved health-data format into the existing record pathway. This is a proposal, not a repository fact.

No assumption resolves `UQ-001`; the current 30-day behavior must not be silently reused for health data.
