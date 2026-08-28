---
name: discover-domain
description: Use when a dossier needs stakeholder goals, domain language, constraints, evidence, assumptions, contradictions, or unresolved questions established before use cases are written.
---

# Discover Domain

Build a trustworthy account of the problem domain. Discovery is sufficient when another capable agent can explain what outcome matters, to whom, under which constraints, and where uncertainty remains without inventing missing facts.

## Contract

Input: initialized dossier, human request, stakeholders or proxies, repository evidence, approved sources, and prior answers.

Output: updated `charter.md`, `stakeholders.md`, `glossary.md`, `assumptions.md`, and `open-questions.md`, with contradictions and provenance visible.

Use [installed resources](../../references/installed-resources.md), [the dossier contract](../../references/artifact-contract.md), and the epistemic categories defined by `align-project`.

## Pass 1: outcome and boundary

Separate the request into:

- current situation and observable pain;
- desired outcome and how a stakeholder notices improvement;
- explicit non-goals;
- scope boundary and neighboring systems;
- deadline, policy, budget, operational, legal, compatibility, and security constraints;
- consequences of failure and of doing nothing.

Treat requested solution language as a proposal unless it is an explicit fixed constraint. “Build a dashboard” is not yet the goal; discover which decision or activity it must improve.

## Pass 2: stakeholders and authority

For each material stakeholder capture:

- role or group;
- goal and value sought;
- cost, risk, or harm to avoid;
- information supplied or consumed;
- authority: decides, approves, operates, advises, is affected, or is represented by a proxy;
- conflicts with other interests.

Include operators, support, security, compliance, downstream systems, and people affected by failure—not only the primary user. Never invent personal details or decision authority.

## Pass 3: language

Record domain terms in stakeholder language. Distinguish business concepts from current implementation names. For overloaded or disputed terms, preserve competing definitions and their sources rather than choosing the neatest wording.

## Pass 4: evidence

Inspect relevant code, docs, interfaces, schemas, incidents, analytics, policies, and examples. Record a source path or supplied reference for important observations. Current implementation proves what exists, not what stakeholders intend.

When claims conflict, consider evidence strength:

1. current explicit authoritative decision;
2. binding policy or contract;
3. directly observed behavior or repository artifact;
4. named stakeholder statement;
5. historical documentation;
6. agent inference.

Lower-ranked evidence may reveal a real contradiction; never discard it silently.

## Pass 5: uncertainty register

Every material uncertainty belongs in one of these forms:

- assumption: provisional belief, impact if false, validation owner/path;
- contradiction: incompatible claims, affected outcome, decision owner;
- open question: missing information, why it matters, next person/source.

Do not disguise a recommendation as an assumption. Do not close a question because a plausible answer can be imagined.

## Interview loop

Ask one question at a time:

1. state the current interpretation briefly;
2. name the uncertainty or contradiction;
3. ask a concrete question and say what decision it affects;
4. record the reply as a stakeholder statement;
5. record any agent inference separately;
6. update linked artifacts before continuing.

Offer two or three interpretations when helpful, without forcing a false choice. If the human says “I don't know,” record it and identify a safe experiment, owner, or reversible assumption.

## Completion check

Read the artifacts and confirm:

- charter states problem, outcomes, non-goals, scope, and constraints;
- every important outcome belongs to a stakeholder;
- approval and conflict authority are visible;
- key terms are defined or explicitly disputed;
- repository observations cite sources;
- assumptions state impact and validation path;
- contradictions remain visible;
- open questions explain why they matter;
- no implementation choice is disguised as a fact.

If a material goal, constraint, or authority question remains unanswered, stay in discovery. Otherwise add `discover` to `completed_phases` and set `current_phase` to the next material phase. Synchronize `snapshot_paths` only in exact-snapshot mode.

Next transition: `alignment:write-use-cases`.
