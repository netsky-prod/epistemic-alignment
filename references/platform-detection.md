# Platform detection and presentation

Detect the host before presentation. Canonical dossier files remain the source in every host.

| Host capability | Presentation | Decision channel |
| --- | --- | --- |
| Codex with Sites | ChatGPT Site under `alignment-review/site/` | current Codex conversation |
| Claude with Artifacts | Artifact derived from dossier | current Claude conversation |
| OpenCode or Qwen Code | local static site and preview command | current host conversation |
| No renderer | Markdown dossier plus file links | current host conversation |

Every presentation follows [the stakeholder presentation method](presentation.md): narrative order, substantive evidence excerpts, visible uncertainty, findings before readiness, and a clear decision boundary.

Build and inspect a draft first. Publishing or updating a hosted Site needs separate explicit human consent. Record adapter, status, and location through the resolved installed helper only after the presentation is ready.

Host-specific constraints:

- Codex Sites: copy the unbound bundled template into the project, never a maintainer `project_id`.
- Claude Artifact: keep the Artifact derived/read-only and make canonical dossier references visible.
- OpenCode/Qwen: create a local static review project and provide an explicit local preview command; do not require hosted infrastructure.
- Fallback: use a navigable Markdown review with excerpts and file/ID references rather than claiming a richer renderer exists.

The decision channel is always the current human conversation, never the presentation UI.
