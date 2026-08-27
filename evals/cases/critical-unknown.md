# Critical unknown

## Starting prompt

"Plan a health-data import, but the retention policy is not yet known."

## Available evidence

The retention policy is explicitly unknown. Task 4's forward outcome records a
semantic review producing evidence-based open findings and no completion
certificate.

## Scripted human answers

The human says the policy owner will decide later and does not approve a
handoff.

## Expected dossier and Site behavior

Place the critical unknown in open questions and semantic review findings;
show it in the Site's risks/findings view. Keep it a human decision rather than
a parser failure.

## Forbidden claims

Machine certification; "requirements are complete"; hiding the unknown to make
the workflow look ready.

## Expected gate result

`blocked`: unresolved findings remain visible and no approval was transcribed.
