---
{"artifact":"context","entities":[]}
---
# Context

The proposed export workflow interacts with Finance and Support policy
stakeholders. The policy boundary is unresolved: Finance requires
irreversibility, while Support requires a cancellation window. The COO is the
future decision owner. This is a context proposal, not a settled architecture.

```mermaid
flowchart LR
  Finance[Finance requirement] --> Export[Proposed export workflow]
  Support[Support requirement] --> Export
  COO[COO future decision owner] -. resolves CON-001 .-> Export
```

Textual fallback: Finance and Support both constrain the export workflow; the
COO is expected to resolve the conflict before implementation.
