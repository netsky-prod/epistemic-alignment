---
{"artifact":"charter","entities":["GOAL-001","FACT-001","FACT-002","FACT-003","UQ-001"]}
---
# Charter

## Goal

Align stakeholders on a proposed health-data import flow for the existing product before implementation planning. The human confirmed the outcome (support the import), but did not approve the dossier and left retention for decision.

## Evidence boundary

- `FACT-001` — Repository fact supplied for this run: the current importer accepts CSV input.
- `FACT-002` — Repository fact supplied for this run: imported records are stored for 30 days.
- `FACT-003` — Repository fact supplied for this run: the current product already has an importer and record storage behavior; these facts describe current behavior, not permission for the proposed change.
- `STMT-001` — Human statement: the desired product outcome is a health-data import.
- `STMT-002` — Human statement: retention for health data remains open; no retention value or policy was confirmed.

## Constraints and uncertainty

- Health data may require additional privacy, security, and governance review; this is a risk/inference, not a repository fact.
- `UQ-001` (critical): What retention policy and deletion behavior govern health-data records?
- `UQ-002`: Which source formats and validation rules are in scope beyond the current CSV path?

## Current phase

Discovery, use-case, behavior, architecture, and semantic review artifacts are drafted. A derived Site review payload is a draft/reference only. The approval gate is blocked because no current explicit human decision was supplied and `UQ-001` is unresolved.
