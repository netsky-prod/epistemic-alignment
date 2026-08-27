# Epistemic Alignment

Epistemic Alignment is a Codex plugin for reaching a shared, inspectable
understanding of a complex software initiative before implementation planning.
It guides discovery, Cockburn use cases, BDD examples, C4 architecture, ADRs,
semantic review, a stakeholder-facing review Site, explicit human approval,
and a hash-verified handoff to Superpowers.

The product is the agent workflow: eight substantial skills guide inquiry,
goal modeling, examples, responsibility design, independent review, and a
human decision. A thin dependency-free Python helper only initializes files,
binds the reviewed snapshot to the current decision, rejects stale approval,
and writes the handoff. It is not a requirements compiler or semantic
validator.

## What is included

- Eight `alignment:*` skills, with `alignment:align-project` as the front door.
- Deep Cockburn, BDD, C4/ADR, epistemic-discovery, semantic-review, and
  stakeholder-presentation methods.
- A Python 3.9-compatible `scripts/alignment` helper with no third-party runtime
  dependencies.
- Portable Markdown, Gherkin, Mermaid, and ADR templates.
- A read-only ChatGPT Sites adapter for Codex stakeholder review.
- A complete release example under `examples/approved-project/`.
- Human-inspectable scenarios under `evals/`; these are examples, not release
  proof or machine certification.

## Quick start

Install the local plugin using [the installation guide](docs/installation.md),
start a new Codex task, and ask:

> Use alignment:align-project to align this initiative before implementation
> planning.

The normal flow is:

```text
qualify -> discover -> use cases -> behavior -> architecture
        -> semantic review -> presentation -> human decision -> handoff
        -> superpowers:brainstorming
```

Canonical project documents live in `alignment/`. The generated review project
lives in `alignment-review/site/`. Approval happens only in the host
conversation; the Site has no approval button or persistence. After the Site,
the stakeholder can reply simply `approved`, `changes_requested`, or
`rejected`; the agent binds that reply to the current issued digest internally.

## How installed skills use the helper

Skills resolve the helper and Site template relative to their installed plugin
path. They do not expect the target repository to contain this plugin's
`scripts/` or `adapters/` directories. The commands below are the underlying
interface; normal users interact with the agent and reply to the review in
plain language.

## Helper commands

```sh
scripts/alignment init <project-root> --project-id <id> --title <title>
scripts/alignment snapshot <project-root> --json
scripts/alignment issue-review <project-root> \
  --adapter codex-sites --status presented --location alignment-review/site
scripts/alignment decide <project-root> \
  --decision approved --reviewer <label> --provenance human-message \
  --review-hash <exact-issued-hash>
scripts/alignment check <project-root> --json
scripts/alignment handoff <project-root>
```

See [usage](docs/usage.md) for the phase outputs and gate protocol,
[recovery](docs/recovery.md) for restart and stale-review handling, and the
[trust model](docs/trust-model.md) before relying on an approval record.

## Verification

The plugin helper itself has no third-party runtime dependencies. The
plugin-creator validator separately imports PyYAML, so run it from a dedicated,
pinned validator environment. The full local release check is:

```sh
git diff --check
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m unittest tests.test_release -v
pnpm --dir adapters/codex-site/template test
pnpm --dir examples/approved-project/alignment-review/site test
scripts/alignment snapshot examples/approved-project --json
scripts/alignment check examples/approved-project --json
! rg -n "class Entity|ValidationReport|the semantic validator passed|coverage.*complete" src tests
git status --short

alignment_validator_venv="$(mktemp -d)"
python3 -m venv "$alignment_validator_venv"
"$alignment_validator_venv/bin/python" -m pip install \
  --disable-pip-version-check "PyYAML==6.0.2"
alignment_plugin_creator="${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator"
"$alignment_validator_venv/bin/python" \
  "$alignment_plugin_creator/scripts/validate_plugin.py" .
```

Publishing the review Site is optional and requires separate explicit human
consent. This repository does not publish a Site or plugin automatically.

## Release metadata

The recommended GitHub repository name is `epistemic-alignment`, and the first
release tag is `v0.1.0`. The manifest intentionally omits repository and
homepage fields until an actual remote exists. Release screenshots are included
as plugin assets and retained with their pixel metadata in
`artifacts/release/e2e.json`.

## Documentation

- [Installation, reinstall, and removal](docs/installation.md)
- [Workflow and command usage](docs/usage.md)
- [Recovery and restartability](docs/recovery.md)
- [Trust boundary and limitations](docs/trust-model.md)
- [Renderer contract and future adapters](docs/adapters.md)
- [Release history](CHANGELOG.md)

The package is licensed under the MIT License.
