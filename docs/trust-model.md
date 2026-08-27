# Trust model

Epistemic Alignment separates human/model judgment from deterministic process
mechanics. This boundary is the central safety property of version 0.1.0.

## What the helper proves

- The manifest uses a supported shape and declared paths remain within the dossier.
- Included UTF-8 files produce a deterministic `sha256-v1` snapshot.
- The issued, rendered, human-approved, current, and handed-off hashes are equal.
- A presentation has status `presented` or `published` before approval.
- The stored approval provenance is `human-message`.
- A later included-file change makes the approval stale and blocks handoff.
- A generated handoff is a regular non-symlink file at the expected path whose
  exact bytes match the `content_sha256` stored by the helper.

## What it does not prove

- That goals, use cases, BDD examples, C4 models, or ADRs are correct or complete.
- That traceability links or scenario coverage are semantically sufficient.
- That contradictions or open questions are resolved.
- That stakeholders reached consensus.
- That the reviewer label is an authenticated identity or cryptographic signature.
- That Codex intercepts every relevant prompt.

Skills use model judgment to author and skeptically review semantics. Humans
decide whether recorded findings are resolved or acceptable. The helper never
parses those documents into a truth database, calculates coverage, or replaces review.

## Human-only approval

An approved decision is authorized only by an explicit human message in the
current interaction after the review reference, findings, and exact digest are
shown. Prior permission, silence, generic encouragement, agent confidence,
pre-edited state, and Site controls are insufficient. The agent may transcribe
the decision but may not create it. The human can reply simply `approved`,
`changes_requested`, or `rejected`; the agent binds that current reply to the
current issued digest internally and supplies the digest to the helper CLI.

The reviewer label is descriptive only. Consumers that require authenticated
identity, signatures, quorum, or regulated records must add an external
approval system; version 0.1.0 makes no such claim.

## Snapshot scope

Only `manifest.yaml` metadata and files listed in `snapshot_paths` contribute
to the digest. `review-state.json`, generated `handoff.md`, presentation output,
timestamps, renderer state, and stored hashes are excluded. Skills must verify
that every current reviewable dossier file is included before presentation.
This membership check is a human/method responsibility, not semantic certification.

## Presentation and publishing

The Codex Site is derived and read-only. It has no approval button,
authentication, persistence, or database bindings. Local generation and
inspection are not publication and not approval. Hosting or updating a Site
requires separate explicit human consent and cannot manufacture presentation
or decision state.

## Downstream trust

A verified `handoff.md` proves only that the bytes in the included dossier
match the snapshot a human explicitly approved. Superpowers must still use
brainstorming, planning, TDD, review, and verification. The handoff is required
context, not permission to skip downstream engineering controls. Verification
also binds the exact helper-generated handoff bytes; retaining the approved
digest as text inside a modified or substituted handoff is insufficient.
