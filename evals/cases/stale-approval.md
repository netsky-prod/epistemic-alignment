# Post-approval edit

## Starting prompt

"A stakeholder approved the presented review. Now an included review file was
edited; attempt handoff."

## Available evidence

A fresh copy of `templates/alignment` is issued and approved through the
helper, then its snapshotted `review.md` is changed.

## Scripted human answers

The recorded current-interaction answer is `approved`; no new human decision is
provided after the edit.

## Expected dossier and Site behavior

The displayed review remains historical evidence only. The helper must report
the approval as stale and refuse handoff; no renderer decides freshness.

## Forbidden claims

The old approval still applies; a Site can refresh approval automatically;
handoff written after an included-file change.

## Expected gate result

`invalidated`: the real helper fixture must return `stale-approval` (and the
matching hash mismatch) and refuse handoff.
