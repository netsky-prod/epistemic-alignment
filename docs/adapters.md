# Renderer adapters

Canonical alignment artifacts are portable. A renderer creates a derived
review surface without owning decisions or mutating the dossier.

## Common contract

Every adapter receives the dossier directory, complete included-path list and
issued `sha256-v1` digest, human-readable semantic review, and host
capabilities. It returns an adapter name/version, generated location or
reference, `draft`/`presented`/`published` status, rendered digest, and warnings.

All adapters must expose the same evidence, uncertainty, contradictions,
questions, findings, and exact digest. Every material summary links to a
substantive evidence excerpt or served read-only source view—not merely a
repeated path label. Presentation is never approval. See the full
[adapter contract](../adapters/adapter-contract.md).

## Codex — version 0.1.0

The production adapter resolves and copies the unbound installed
`adapters/codex-site/template` to
`alignment-review/site`, populates `public/review.json`, builds it with Sites,
and visually checks desktop and narrow layouts. It does not inherit a
maintainer deployment ID. The Site is read-only and the host conversation
remains the decision channel. Publication is optional, private by default, and
requires explicit consent.

## Claude roadmap

The planned Claude adapter renders the same input as an Artifact, preserves
textual evidence references and uncertainty labels, and returns an Artifact
reference plus rendered hash and warnings. Installation metadata, invocation,
visual QA, and current-message approval transcription require a separate
implementation cycle. Details: [Claude roadmap](../adapters/claude.md).

## OpenCode roadmap

The planned OpenCode adapter uses a shared local static renderer with explicit
preview commands and OpenCode-specific skill/extension metadata. It must bind
the preview to the exact dossier digest and keep approval in the host
conversation. Details: [OpenCode roadmap](../adapters/opencode.md).

## Qwen Code roadmap

The planned Qwen Code adapter reuses the local static renderer while providing
separate Qwen extension/skill metadata, invocation, and verification guidance.
It must not claim adapter parity until independently installed and tested.
Details: [Qwen Code roadmap](../adapters/qwen-code.md).

Claude, OpenCode, and Qwen Code are road maps, not production adapters in the
Codex-first release.
