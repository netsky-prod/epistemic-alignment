---
name: build-review
description: Use when a semantically reviewed dossier needs a stakeholder-facing presentation that makes the proposed understanding, evidence, uncertainty, architecture, findings, and decision boundary easy to inspect.
---

# Build Review

Turn the canonical dossier into a decision-quality stakeholder review. The presentation must help a person understand and challenge the model; it is not a decorative report and never records approval.

## Contract

Input: current dossier, `review.md`, manifest, snapshot, target host capabilities, and any existing presentation.

Output: a read-only draft presentation, its location, an issued review snapshot, and one clear request for stakeholder review.

Use [installed resources](../../references/installed-resources.md), [platform detection](../../references/platform-detection.md), [presentation method](../../references/presentation.md), and [thin approval](../../references/approval.md).

Resolve the bundled Site template from `$ALIGNMENT_PLUGIN_ROOT/adapters/codex-site/template`; never look for it beneath the target project.

## Preconditions

1. Read the complete dossier and `review.md` semantically.
2. Verify that every human-authored reviewable dossier file is in `snapshot_paths`.
3. Rebuild when source files, findings, or current snapshot differ from the existing presentation.
4. Do not hide open findings to make the presentation appear ready.

If open blocking findings prevent meaningful review, present them explicitly and ask whether the stakeholder wants revision before issuance. A review Site may show unreadiness; it must not fabricate readiness.

## Design the stakeholder narrative

The presentation answers these questions in order:

1. What problem and outcome are we aligning on?
2. Who is affected, and who has authority?
3. What are the priority actor goals and guarantees?
4. What concrete examples define important behavior and boundaries?
5. How are responsibilities divided and why?
6. Which decisions, risks, assumptions, and contradictions remain?
7. What did independent review find?
8. What exactly would approval authorize—and what would it not authorize?

Use progressive disclosure. The first screen should orient a stakeholder; deeper sections should expose evidence rather than overwhelm them with raw files.

## Evidence model

Every material summary claim carries a source path or stable ID. A traceability target must show:

- the source path/ID;
- a substantive human-readable excerpt or faithful presentation of the cited evidence;
- its epistemic status where relevant: confirmed, proposed, assumed, conflicting, or open;
- links to related goal/use-case/scenario/architecture/finding IDs.

Do not make a link that merely scrolls to a duplicate path label. Do not link to unserved local Markdown routes. The Site is derived presentation data, so excerpts never replace canonical dossier files.

## Codex Sites adapter

On Codex with Sites:

1. Copy the unbound bundled template to `$PROJECT_ROOT/alignment-review/site/`. Do not copy a maintainer deployment `project_id`.
2. Populate `public/review.json` with exactly these top-level keys: `project`, `summary`, `stakeholders`, `useCases`, `behavior`, `architecture`, `decisions`, `risks`, `findings`, and `snapshot`.
3. Put the evidence index beneath an existing nested key, preserving the ten-key contract. Include a substantive excerpt for every referenced source.
4. Render seven anchored views: summary, stakeholders, use cases, behavior, architecture, decisions-and-risks, and review-readiness.
5. Label proposed, uncertain, assumed, open, accepted, and conflicting material in visible text—not color alone.
6. Show findings before readiness. Provide C4 Mermaid source plus a textual responsibility fallback.
7. Keep all interaction read-only: navigation, expansion, filtering, and copy are allowed; approval buttons, authentication, comments, persistence, databases, and decision mutations are not.

For Claude Artifacts, OpenCode/Qwen local preview, or Markdown fallback, preserve the same narrative, evidence, uncertainty, findings, and decision boundary using the host mechanism described in platform detection.

## Inspect the draft

Inspect content and presentation at desktop and narrow widths. Check:

- headings and keyboard navigation;
- text contrast and visible focus;
- diagrams plus fallback text;
- every evidence reference reaches substantive content;
- no dossier path or user content became unsafe executable markup;
- findings and uncertainty are not visually minimized;
- the snapshot displayed is the current snapshot of the rendered source dossier.

Do not publish or update a hosted Site without separate explicit human consent. Local build/preview and private draft inspection are not approval.

## Issue the review

After the draft is exact, run through the resolved bundled helper:

```sh
"$ALIGNMENT_HELPER" snapshot "$PROJECT_ROOT" --json
"$ALIGNMENT_HELPER" issue-review "$PROJECT_ROOT" --adapter <adapter> --status presented --location <reference>
```

The displayed digest must equal the issued/current digest, but the human never needs to copy it. Add `presentation` to `completed_phases`, set `current_phase` to `approval`, and show the stakeholder:

- presentation location;
- open/material findings and accepted limitations;
- a short statement of what approval means;
- an invitation to inspect and request changes.

A Site view, positive reaction, prior design permission, or absence of objections is not approval.

Next transition: `alignment:approve-handoff`.
