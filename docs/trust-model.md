# Trust model

Epistemic Alignment separates human/model judgment from optional process mechanics. No mode turns a dossier into proof of correctness.

## What human review establishes

An explicit current human message may establish only that the presented dossier is an adequate basis for downstream brainstorming, including any visibly accepted limitations. It does not establish semantic completeness, implementation correctness, security, estimates, consensus, authenticated identity, or regulatory compliance.

Silence, generic prior permission, a Site control, agent confidence, edited state, test fixtures, and approval of the plugin itself are not dossier approval.

## Conversational binding

Conversational binding is the default when the stakeholder and agent review continuously and no material exact-version requirement exists. The handoff records the presentation reference, reviewed sources, current-message provenance, findings, remaining uncertainty, and recommended downstream rigor.

This mode does not claim cryptographic freshness or exact-byte identity. A material source or finding change before delivery invalidates the conversational decision and requires re-presentation.

## Exact-snapshot binding

Exact-snapshot mode is opt in for version-bound approval, regulated/audited evidence, material stale-version risk across asynchronous or multi-writer review, or difficult-to-reverse downstream action.

The helper can establish that:

- declared paths remain inside the dossier;
- included UTF-8 files produce a deterministic `sha256-v1` snapshot;
- issued, rendered, approved, current, and handed-off digests agree;
- approval provenance is `human-message`;
- later included-file changes stale the approval;
- generated handoff bytes match the helper's recorded content hash.

It cannot judge goals, use cases, BDD, C4, ADRs, traceability, uncertainty, stakeholder consensus, or reviewer identity. Consumers requiring authentication, signatures, quorum, or regulated records need an external system.

## Presentation and publishing

The review Site is derived and read-only. It has no approval button, authentication, persistence, or decision mutation. Local generation is not publication. Hosting or updating requires separate explicit human consent and cannot manufacture approval.

## Downstream process

The handoff includes a recommended rigor level plus retained and omitted gates. Superpowers treats this as current evidence and recalibrates rather than blindly replaying every workflow. Irreversible, destructive, security-sensitive, and external actions retain hard gates. A local reversible prompt change does not inherit release, cryptographic, unit-test, or review-fanout ceremony without a named risk or claim that needs it.
