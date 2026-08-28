# Human semantic-review method

Semantic review challenges whether the dossier tells one coherent, evidence-backed story. It is performed with judgment and recorded for stakeholders; it is not a compiler or certificate.

## Seven review lenses

1. **Goals and authority:** outcomes, non-goals, stakeholders, conflicts, and decision rights.
2. **Epistemic integrity:** facts/statements/inferences/assumptions remain distinct; contradictions and missing evidence are visible.
3. **Use-case quality:** goal altitude, actor intent, guarantees, material extensions, and recovery.
4. **Behavior coverage:** critical paths/rules/boundaries have observable examples; proposed behavior is labelled.
5. **Architecture responsibility:** priority behavior has owners; boundaries, data, trust, failure, and operations are explained.
6. **Decision quality:** material choices expose drivers, alternatives, consequences, risks, and invalidating assumptions.
7. **Stakeholder and process readability:** a non-author can understand the proposal, uncertainty, findings, requested decision, binding mode, and why retained/omitted gates match the actual risk.

## Bidirectional traceability

Walk forward:

```text
stakeholder interest → goal → use case → scenario → responsibility → decision
```

Walk backward:

```text
container/component/ADR → scenario/risk → use case → stakeholder outcome
```

Missing links are findings when they hide rationale or leave behavior unowned. Cross-cutting concerns may link to several goals rather than exactly one.

## Finding record

```markdown
| ID | Severity | Finding | Evidence | Impact | Owner / action | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| FINDING-001 | material | ... | `file#section`, `UC-001` | ... | ... | open |
```

- **Blocking:** meaningful stakeholder approval is not possible yet.
- **Material:** approval may proceed only with visible resolution or accepted limitation.
- **Advisory:** useful improvement that does not distort the decision boundary.

Dispositions:

- `open` — unresolved;
- `accepted limitation` — human accepts named consequence;
- `resolved` — source evidence changed and is linked;
- `superseded` — replaced by a newer finding/decision.

## Reviewer rules

- Cite source artifacts, not only conclusions.
- Explain stakeholder/architecture impact, not stylistic preference.
- Repair substantive errors in canonical sources, then update the finding.
- Preserve scope and missing perspectives.
- Never convert “no findings observed” into proof of correctness.
- Never close a contradiction by choosing the most convenient interpretation.
- Separate implementation concerns that belong downstream from alignment gaps that block shared understanding.
- Flag process artifacts or gates whose only justification is prior effort or tool availability; recommend removal instead of hardening unsupported machinery.

## Review output

`alignment/review.md` contains scope/limits, readiness summary, findings, traceability gaps, epistemic gaps, and the stakeholder decision context. It should allow a person to accept a limitation knowingly, request a concrete revision, or reject the model.
