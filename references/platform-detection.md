# Platform detection and presentation

Detect the host before presentation. Canonical dossier files remain the source in every host.

| Host capability | Presentation | Decision channel |
| --- | --- | --- |
| Codex with Sites | ChatGPT Site under `alignment-review/site/` | current Codex conversation |
| Claude with Artifacts | Artifact derived from dossier | current Claude conversation |
| OpenCode or Qwen Code | local static site and preview command | current host conversation |
| No renderer | Markdown dossier plus file links | current host conversation |

Build and inspect a draft first. Publishing or updating a hosted Site needs separate explicit human consent. Record the adapter, status, and location through the thin-gate CLI only after the presentation is ready.
