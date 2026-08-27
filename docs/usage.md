# Usage

## Start or resume

Invoke `alignment:align-project` for a new product, public-interface or
architecture change, ambiguous requirement, multi-stakeholder effort, or work
with material risk. A human may force the full process. A bounded task may skip
only with a written rationale; a skip creates neither approval nor handoff.

The front-door skill inspects `alignment/manifest.yaml` and existing artifacts,
then resumes at the first incomplete phase. The phase outputs are:

1. discovery: charter, stakeholders, glossary, assumptions, and open questions;
2. use cases: Cockburn-style `alignment/use-cases/UC-*.md`;
3. behavior: observable `alignment/features/*.feature` examples;
4. architecture: C4 Markdown/Mermaid and `alignment/decisions/ADR-*.md`;
5. semantic review: human-readable findings in `alignment/review.md`;
6. presentation: a derived, read-only `alignment-review/site/`;
7. decision and handoff: exact-snapshot approval and `alignment/handoff.md`.

Skills ask one material question at a time and visibly distinguish facts,
stakeholder statements, inferences, assumptions, contradictions, and open
questions. Scenario examples in `evals/` illustrate this practice but are not
machine assertions or release authority.

## Thin helper

The launcher works from the plugin checkout or installed plugin cache:

```sh
scripts/alignment --version
```

Initialize once:

```sh
scripts/alignment init <project-root> --project-id <id> --title <title>
```

The initializer exits `0` on success and refuses to overwrite an existing
dossier with exit `2`. Author the dossier through the skills, then inspect the
current mechanical snapshot:

```sh
scripts/alignment snapshot <project-root> --json
```

Snapshot returns `0` and an `algorithm`, `digest`, and sorted `paths` array. An
unsafe, duplicate, missing, non-file, escaping, or invalid UTF-8 included path
returns exit `2`. The helper normalizes text line endings; it does not judge the
meaning or completeness of any document.

## Present and decide

`alignment:build-review` copies the Codex Site template, replaces
`public/review.json` from the dossier, builds and inspects it, and checks that
the displayed hash equals the current snapshot. Draft generation and visual
inspection do not publish. Publishing or updating requires separate explicit
human consent.

Once the stakeholder has actually seen the review, issue it:

```sh
scripts/alignment issue-review <project-root> \
  --adapter codex-sites --status presented --location alignment-review/site
```

Show the location, `review.md` findings, and exact issued digest. In the same
interaction ask for exactly one current decision: `approved`,
`changes_requested`, or `rejected`. The human does not need to repeat or copy
the digest; the agent binds that reply internally to the current issued digest.
Only then may the agent transcribe the decision and bound digest through the
helper:

```sh
scripts/alignment decide <project-root> \
  --decision approved \
  --reviewer "<human-provided label>" \
  --provenance human-message \
  --review-hash "<exact-issued-digest>" \
  --acknowledged-finding "<finding ID>"
```

`decide` returns `0` only for a valid record and exit `2` for malformed or
stale input. `approved` additionally requires a presented/published review,
human-message provenance, and equality of issued, rendered, supplied, and
current hashes. Never infer approval from silence, a prior design approval, an
agent statement, or a Site interaction.

## Check and hand off

```sh
scripts/alignment check <project-root> --json
scripts/alignment handoff <project-root>
```

`check` exits `0` with `ready: true` or `1` with stable mechanical reasons such
as `decision-not-approved`, `presentation-not-presented`, `non-human-provenance`,
`stale-approval`, `hash-mismatch`, `handoff-state-missing`,
`handoff-file-invalid`, or `handoff-digest-mismatch`. `handoff` exits `0` only
after the gate is ready, writes the exact approved digest into
`alignment/handoff.md`, and records a SHA-256 binding to those exact handoff
bytes; it exits `2` otherwise.

The next step is `superpowers:brainstorming` with `handoff.md` and the dossier
as required context. If Superpowers is unavailable, preserve the verified
handoff and report delivery as pending rather than bypassing the dependency.
