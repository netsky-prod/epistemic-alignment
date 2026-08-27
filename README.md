# Epistemic Alignment

Epistemic Alignment is a Codex plugin for reaching a shared, inspectable
understanding of a complex software initiative before implementation planning.
It guides discovery, Cockburn use cases, BDD examples, C4 architecture, ADRs,
semantic review, a stakeholder-facing review Site, explicit human approval,
and a hash-verified handoff to Superpowers.

The package deliberately keeps a thin deterministic boundary. Skills and
people judge meaning; the dependency-free Python helper initializes files,
hashes the reviewed snapshot, records a current human decision, rejects stale
approval, and writes the handoff. It is not a requirements compiler or a
semantic validator.

## What is included

- Eight `alignment:*` skills, with `alignment:align-project` as the front door.
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
pinned validator environment:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
validator_venv="$HOME/.cache/epistemic-alignment/plugin-validator-pyyaml-6.0.2"
python3 -m venv "$validator_venv"
"$validator_venv/bin/python" -m pip install --disable-pip-version-check "PyYAML==6.0.2"
"$validator_venv/bin/python" \
  /Users/darasokolovskaa/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
scripts/alignment snapshot examples/approved-project --json
scripts/alignment check examples/approved-project --json
pnpm --dir examples/approved-project/alignment-review/site test
```

Publishing the review Site is optional and requires separate explicit human
consent. This repository does not publish a Site or plugin automatically.

## Documentation

- [Installation, reinstall, and removal](docs/installation.md)
- [Workflow and command usage](docs/usage.md)
- [Recovery and restartability](docs/recovery.md)
- [Trust boundary and limitations](docs/trust-model.md)
- [Renderer contract and future adapters](docs/adapters.md)

The package is licensed under the MIT License.
