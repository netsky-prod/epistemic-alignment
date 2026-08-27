# Conflict eval transcript

Each record follows the mechanical eval event schema; it does not certify dossier semantics.

```json-event
{"id":"E001","role":"human","type":"request","evidence":[],"body":"Capture Finance's irreversible-export requirement and Support's cancellation-window requirement without choosing a policy."}
```
```json-event
{"id":"E002","role":"human","type":"human-answer","evidence":[],"body":"Both positions are current, resolution belongs to the COO, and no current explicit approval was supplied."}
```
```json-event
{"id":"E003","role":"agent","type":"command","evidence":[],"action_id":"A001","operation":"init","argv":["scripts/alignment","init","<run-dir>","--project-id","conflict-export","--title","Irreversible export and cancellation alignment"]}
```
```json-event
{"id":"E004","role":"tool","type":"command-result","evidence":["alignment/manifest.yaml"],"action_id":"A001","exit_code":0,"output":{"alignment":"alignment"}}
```
```json-event
{"id":"E005","role":"agent","type":"command","evidence":[],"action_id":"A002","operation":"snapshot","argv":["scripts/alignment","snapshot","<run-dir>","--json"]}
```
```json-event
{"id":"E006","role":"tool","type":"command-result","evidence":["alignment/manifest.yaml"],"action_id":"A002","exit_code":0,"output":{"algorithm":"sha256-v1","digest":"a4f6ae31caa93949e9909a70978279333e49a8bb5145da86b1d82920fc34d494","paths":["architecture/components.md","architecture/containers.md","architecture/context.md","assumptions.md","charter.md","decisions/ADR-001.md","features/export-cancellation.feature","glossary.md","open-questions.md","review.md","stakeholders.md","use-cases/UC-001.md"]}}
```
```json-event
{"id":"E007","role":"agent","type":"artifact","evidence":["alignment-review/site-review.json"],"artifact_type":"review-surface","path":"alignment-review/site-review.json"}
```
```json-event
{"id":"E008","role":"agent","type":"command","evidence":[],"action_id":"A003","operation":"issue-review","argv":["scripts/alignment","issue-review","<run-dir>","--adapter","codex-sites","--status","presented","--location","alignment-review/site-review.json"]}
```
```json-event
{"id":"E009","role":"tool","type":"command-result","evidence":["alignment/review-state.json"],"action_id":"A003","exit_code":0,"output":{"algorithm":"sha256-v1","digest":"a4f6ae31caa93949e9909a70978279333e49a8bb5145da86b1d82920fc34d494"}}
```
```json-event
{"id":"E010","role":"agent","type":"command","evidence":[],"action_id":"A004","operation":"check-gate","argv":["scripts/alignment","check","<run-dir>","--json"]}
```
```json-event
{"id":"E011","role":"tool","type":"command-result","evidence":["alignment/review-state.json"],"action_id":"A004","exit_code":1,"output":{"digest":"a4f6ae31caa93949e9909a70978279333e49a8bb5145da86b1d82920fc34d494","ready":false,"reasons":["review-state-invalid"]}}
```
```json-event
{"id":"E012","role":"agent","type":"outcome","evidence":["alignment/review-state.json"],"body":"The review surface was presented, the helper gate remained blocked, and no approval or handoff was recorded."}
```
