---
name: build-review
description: Use when a reviewed alignment dossier needs a stakeholder-facing presentation that exposes evidence references, uncertainty, findings, and snapshot readiness.
---

# Build Review

Render a derived review surface while keeping dossier files canonical. Read [platform detection](../shared/references/platform-detection.md) and [thin approval](../shared/references/approval.md).

## Contract

Input: the current `alignment/` dossier, `review.md`, manifest, and `sha256-v1` snapshot. Output: a read-only draft presentation, its location, and an issued review snapshot. The presentation never records a decision or changes approval state.

1. Inspect the dossier, `review.md`, manifest, and existing presentation state. Rebuild whenever the current snapshot or findings differ from the presented view. Verify every current reviewable dossier file is listed in manifest `snapshot_paths`.
2. Detect the host. On Codex with Sites, copy `adapters/codex-site/template` to `alignment-review/site/`, read the dossier semantically, and replace `alignment-review/site/public/review.json`. Populate exactly these top-level keys: `project`, `summary`, `stakeholders`, `useCases`, `behavior`, `architecture`, `decisions`, `risks`, `findings`, and `snapshot`. This payload is presentation input, not a certificate or a canonical dossier.
3. Include the current `sha256-v1` digest verbatim in `snapshot`; retain evidence references and IDs. Render all seven anchored views: summary, stakeholders, use cases, behavior, architecture, decisions-and-risks, and review-readiness. Evidence references are non-clickable path/ID text because canonical dossier files are not served by the Site. Keep proposed, uncertain, and conflicting material textually labelled; show findings above snapshot readiness; provide C4 Mermaid source with a textual fallback. Do not add approval controls, authentication, persistence, or database bindings.
4. Build and inspect the draft with Sites. Confirm the displayed snapshot digest exactly equals `scripts/alignment snapshot <root> --json` for the content rendered. Do not publish or update a hosted Site during this step.
5. Only after the rendered digest is exact and the draft is ready, run `scripts/alignment issue-review <root> --adapter codex-sites --status presented --location alignment-review/site`. The issued hash must be the exact snapshot hash displayed by the Site. For other hosts, create the equivalent derived presentation and use its adapter/location.
6. Show the stakeholder the reference, `alignment/review.md` findings, and issued hash. Hosting or updating a Site requires separate explicit human consent. A draft, build, visual inspection, or Site control is never approval.

Next transition: `alignment:approve-handoff`.
