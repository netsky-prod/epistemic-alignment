# Greenfield alignment

## Starting prompt

Exact request event: "Create an alignment dossier for the greenfield billing
handoff before implementation."

## Available evidence

The request and stakeholder statements only; no existing repository is treated
as a source of truth. Task 4's fresh-context baseline records that controls did
not create the canonical dossier or thin-gate sequence.

## Scripted human answers

Exact human-answer event: "The human supplied the billing goal and did not
supply a current approval decision."

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
