# Alignment scenario evals

This corpus records behavioral expectations for the portable alignment skills and
thin approval gate. It is deliberately not an agent benchmark that declares a
semantic pass: the skill cases preserve expected human-review behavior, while
the two deterministic gate cases are re-executed against freshly copied
fixtures by `scripts/check-evals`.

Run the checker from the repository root:

```sh
scripts/check-evals artifacts/evals/results.json
```

`evals/expected/` contains assertions; `artifacts/evals/results.json` contains
captured output separately. Semantic captures cite the Task 4 fresh-context
baseline/forward outcome record; no raw Task 4 transcript is recreated here.
They are evidence about those recorded runs, not a claim that this checker
replayed a hosted Site or authenticated a human. The checker rejects a
forbidden claim appearing in captured output and re-executes the stale-approval
and self-approval fixtures with the standard-library helper.
