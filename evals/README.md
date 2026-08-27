# Alignment scenario examples

The seven Markdown cases are illustrative, non-authoritative examples of the
alignment workflow and thin approval gate. Five cases have captured semantic
runs under `artifacts/evals/runs/`: `bounded-skip`, `conflict`,
`critical-unknown`, `existing-repo`, and `greenfield`. The
`stale-approval` and `self-approval` cases are case-only deterministic helper
walkthroughs; they intentionally have no captured run directories.
Everything here is provided for manual inspection and discussion only.

These examples are not a proof of behavior, a release gate, or a required
validator. They do not certify dossier semantics, requirement quality,
stakeholder agreement, presentation behavior, or human approval. Product tests
for the deterministic snapshot and approval helper remain the verification
surface for release work.

When reviewing one of the five captured examples, inspect its case Markdown
together with the matching directory under `artifacts/evals/runs/`. For the two
case-only walkthroughs, inspect the scripted helper sequence in the case
Markdown; there is no captured directory to pair with it. Treat captured files
as historical examples: rerun relevant product commands against the current
implementation when evidence about current behavior is required.
