---
name: build-review
description: Use when a reviewed alignment dossier needs a stakeholder-facing presentation that exposes source links, uncertainty, findings, and snapshot readiness.
---

# Build Review

Render a derived review surface while keeping dossier files canonical.

## Contract

Input: current `alignment/` dossier including `review.md`. Output: a draft presentation under `alignment-review/`, a visible reference, and an issued review snapshot. Read [platform detection](../shared/references/platform-detection.md) and [thin approval](../shared/references/approval.md).

1. Inspect the dossier, `review.md`, manifest, and existing presentation state. Rebuild when the source snapshot or findings changed.
2. Detect the host. On Codex use Sites; on Claude use an Artifact; on OpenCode/Qwen Code use a local site; otherwise provide a Markdown view. Include goals, stakeholders, use cases, behavior, C4/ADRs, uncertainty, findings, source links, and the snapshot hash.
3. Build and inspect the draft. Keep proposed, uncertain, and conflicting material visibly labelled; presentation controls do not record decisions.
4. Verify every current reviewable dossier file is listed in manifest `snapshot_paths`; then create the snapshot and issue the review with `scripts/alignment issue-review <root> --adapter <adapter> --status presented --location <reference>`.
5. Request separate explicit human consent before hosting or updating a Site.

Do not treat draft generation or a Site button as approval. Next transition: `alignment:approve-handoff`.
