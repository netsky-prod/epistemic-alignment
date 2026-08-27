# Greenfield alignment

## Starting prompt

"We are starting a multi-stakeholder service with uncertain billing rules. Help
us align before implementation planning."

## Available evidence

The request and stakeholder statements only; no existing repository is treated
as a source of truth. Task 4's fresh-context baseline records that controls did
not create the canonical dossier or thin-gate sequence.

## Scripted human answers

The human answers one material discovery question at a time and does not issue
an approval message during this case.

## Expected dossier and Site behavior

Create the canonical dossier through the skill stages, distinguish assumptions
from stakeholder statements, retain semantic findings in `review.md`, and make
any Site a draft review surface. Do not record a decision or imply that a Site
has been approved.

## Forbidden claims

"the semantic validator passed"; machine approval; a Site approval button as a
decision channel.

## Expected gate result

`blocked`: without a current explicit human message and matching presented
snapshot, no handoff is available.
