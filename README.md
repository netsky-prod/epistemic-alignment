# Epistemic Alignment

Epistemic Alignment is a Codex plugin for reaching a shared, inspectable
understanding of a complex software initiative before implementation planning.
It guides discovery, Cockburn use cases, BDD examples, C4 architecture, ADRs,
semantic review, a stakeholder-facing review Site, explicit human approval,
and a risk-calibrated handoff to Superpowers.

The product is the agent workflow: eight substantial skills guide inquiry,
goal modeling, examples, responsibility design, independent review, and a
human decision. The workflow records which phases and gates are justified,
which are intentionally omitted, and how much downstream process is warranted.
A thin dependency-free Python helper is available when exact-snapshot binding
is materially required; ordinary review uses conversational approval without a
hash ceremony. The helper is not a requirements compiler or semantic validator.

## What is included

- Eight `alignment:*` skills, with `alignment:align-project` as the front door.
- Deep Cockburn, BDD, C4/ADR, epistemic-discovery, semantic-review, and
  stakeholder-presentation methods.
- An optional Python 3.9-compatible exact-snapshot helper with no third-party
  runtime dependencies.
- Portable Markdown, Gherkin, Mermaid, and ADR templates.
- A read-only ChatGPT Sites adapter for Codex stakeholder review.
- A complete worked exact-snapshot example under `examples/approved-project/`.

## Quick start

Install the local plugin using [the installation guide](docs/installation.md),
start a new Codex task, and ask:

> Use alignment:align-project to align this initiative before implementation
> planning.

The normal flow is:

```text
calibrate -> only material alignment phases -> presentation
          -> human decision -> handoff with downstream rigor
        -> superpowers:brainstorming
```

Canonical project documents live in `alignment/`. The generated review project
lives in `alignment-review/site/`. Approval happens only in the host
conversation; the Site has no approval button or persistence. After the Site,
the stakeholder can reply simply `approved`, `changes_requested`, or
`rejected`. Conversational binding is the default; an issued digest is used
only when the process contract names a real exact-version requirement.

## Optional exact-snapshot helper

Skills resolve bundled resources relative to their installed plugin path. They
do not expect the target repository to contain this plugin's `scripts/` or
`adapters/` directories. The commands below are used only by exact-snapshot
mode; normal users interact with the agent in plain language.

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

See [usage](docs/usage.md) for process calibration, phase outputs, and both
decision modes,
[recovery](docs/recovery.md) for restart and stale-review handling, and the
[trust model](docs/trust-model.md) before relying on an approval record.

Publishing the review Site is optional and requires separate explicit human
consent. This repository does not publish a Site or plugin automatically.

## Release metadata

The recommended GitHub repository name is `epistemic-alignment`, and the first
release tag is `v0.1.0`. The manifest intentionally omits repository and
homepage fields until an actual remote exists. Review screenshots are included
as plugin assets.

## Documentation

- [Installation, reinstall, and removal](docs/installation.md)
- [Workflow and command usage](docs/usage.md)
- [Recovery and restartability](docs/recovery.md)
- [Trust boundary and limitations](docs/trust-model.md)
- [Renderer contract and future adapters](docs/adapters.md)
- [Release history](CHANGELOG.md)

The package is licensed under the MIT License.
