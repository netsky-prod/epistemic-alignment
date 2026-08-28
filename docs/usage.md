# Usage

## Start with calibration

Invoke `alignment:align-project` for ambiguous, architecture-changing, stakeholder-heavy, or materially risky work. Before creating a dossier, the skill states a process contract:

- desired deliverables;
- actual material risks and failure stakes;
- reversibility and external effects;
- phases and gates retained or omitted;
- conversational or exact-snapshot review binding;
- recommended downstream rigor: direct, bounded, full, or critical.

Genuinely clear bounded work proceeds directly without dossier or handoff. Aligned work creates only artifacts that resolve a named material question or risk. The available methods are:

1. discovery: charter, stakeholders, glossary, assumptions, and open questions;
2. Cockburn use cases when actor goals/interactions matter;
3. BDD examples when observable boundaries or guarantees matter;
4. C4/ADRs when responsibilities, interfaces, or choices matter;
5. semantic review when cross-artifact coherence is a material risk;
6. a read-only stakeholder presentation when a human decision is needed;
7. explicit decision and handoff.

Before another phase or review cycle, the agent names what it will decide or de-risk. Unsupported phases are recorded `not needed`; two cycles with no new material information trigger recalibration.

## Human review

The review surface shows the proposed understanding, evidence, uncertainty, contradictions, findings, binding mode, and downstream-rigor recommendation. The stakeholder replies naturally with `approved`, `changes_requested`, or `rejected`. A Site interaction, silence, old permission, agent confidence, or a test fixture is not approval.

### Conversational binding — default

Use for continuous human review where exact-byte provenance is not materially required. On approval the agent writes `alignment/handoff.md` with the presentation reference, reviewed source paths, current-message provenance, accepted findings, remaining uncertainty, and downstream-rigor recommendation. It explicitly says `not exact-byte bound`.

A material source/finding change before delivery requires re-presentation and a new decision. The agent does not claim cryptographic freshness in this mode.

### Exact-snapshot binding — opt in

Use only when the human requests version-bound approval, regulated/audited evidence needs it, asynchronous or multi-writer review creates material stale-version risk, or downstream action is difficult to reverse.

The installed helper is resolved from the plugin root:

```sh
ALIGNMENT_PLUGIN_ROOT=<resolved installed plugin root>
ALIGNMENT_HELPER="$ALIGNMENT_PLUGIN_ROOT/scripts/alignment"
PROJECT_ROOT=<absolute target project root>

"$ALIGNMENT_HELPER" snapshot "$PROJECT_ROOT" --json
"$ALIGNMENT_HELPER" issue-review "$PROJECT_ROOT" \
  --adapter codex-sites --status presented --location alignment-review/site
"$ALIGNMENT_HELPER" decide "$PROJECT_ROOT" \
  --decision approved \
  --reviewer "<human-provided label>" \
  --provenance human-message \
  --review-hash "<exact-issued-digest>" \
  --acknowledged-finding "<finding ID>"
"$ALIGNMENT_HELPER" check "$PROJECT_ROOT" --json
"$ALIGNMENT_HELPER" handoff "$PROJECT_ROOT"
"$ALIGNMENT_HELPER" check "$PROJECT_ROOT" --json
```

The human never copies the digest or runs commands. Any included-file change invalidates exact-snapshot approval. The helper proves process integrity only, never semantic correctness or authenticated identity.

## Handoff to Superpowers

Superpowers receives `handoff.md`, the process contract, named dossier sources, review findings, and accepted limitations. Exact-snapshot mode also requires a final successful helper check.

The downstream-rigor recommendation is evidence rather than command. Superpowers recalibrates against current risk and may move in either direction. Hard gates remain for irreversible, destructive, security-sensitive, or external actions; planning documents, TDD, review fanout, and release ceremony are not added automatically when the actual claims and risks do not justify them.
