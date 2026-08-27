---
name: model-architecture
description: Use when aligned goals and behavior examples need C4 responsibility views, architecture drivers, boundaries, and material decisions made explicit for stakeholder review.
---

# Model Architecture

Explain how responsibilities support required behavior and where choices create consequences. Architecture is a model of boundaries, ownership, communication, data, trust, and change—not a diagram-shaped implementation guess.

## Contract

Input: discovery, Cockburn use cases, BDD examples, repository facts, constraints, and existing architecture/ADR files.

Output: C4 Markdown views under `alignment/architecture/`, responsibility/behavior maps, and `alignment/decisions/ADR-*.md` for material choices.

Use [installed resources](../../references/installed-resources.md), the complete [C4 and ADR method](../../references/c4.md), and [dossier contract](../../references/artifact-contract.md).

## Extract architecture drivers

Before drawing, list the forces that can change boundaries or technology:

- critical use cases and failure/recovery scenarios;
- volume, latency, availability, consistency, retention, and cost constraints;
- privacy, security, trust, compliance, and audit needs;
- deployment, ownership, support, and operational boundaries;
- integrations and contracts outside the team's control;
- migration and compatibility obligations;
- areas of uncertainty or likely change.

Link every driver to its dossier source. Do not invent numeric quality targets; mark unknown targets as questions.

## Model from outside inward

### 1. System context

Show the software system as one box, the people and external systems that interact with it, and the purpose of each relationship. Include trust or authority boundaries when they affect behavior. Exclude internal components.

Questions the context view must answer:

- whose goal does the system serve?
- what is inside and outside its responsibility?
- which external party owns each dependency?
- what information or authority crosses the boundary?

### 2. Containers

Add containers only when deployable/runtime/store boundaries matter. For each container state:

- responsibility in domain terms;
- interactions and important data ownership;
- execution/deployment boundary;
- supporting use cases/scenarios;
- material quality or trust concern;
- owning team or unknown owner.

Do not create a container per framework layer. A database is not automatically a separate stakeholder responsibility, but its ownership, retention, or consistency may make it material.

### 3. Components

Add a component view only inside a container whose internal responsibility split affects a decision, risk, ownership boundary, or important behavior. Stop before classes, functions, endpoints, or speculative patterns.

## Responsibility-to-behavior mapping

Beside each view maintain a table:

| Element | Responsibility | Supports | Depends on | Failure/recovery | Open concern |

Walk every priority scenario through the model:

1. where does the initiating event enter?
2. which element owns each business responsibility?
3. where is authoritative state held?
4. what crosses a trust or consistency boundary?
5. how is the stakeholder-visible failure/recovery outcome produced?
6. which responsibility is missing, duplicated, or ambiguous?

If no element owns an outcome, the architecture is incomplete. If two elements own it, record the conflict rather than choosing silently.

## Material decisions

Create an ADR when a choice is difficult to reverse, changes a public contract, allocates responsibility, introduces a major dependency, changes data/trust boundaries, or materially affects quality attributes.

An ADR records:

- status and decision owner;
- context and linked drivers;
- decision in concrete terms;
- alternatives genuinely considered;
- positive and negative consequences;
- risks, mitigations, and follow-up validation;
- assumptions that could invalidate the choice.

Do not write an ADR to retroactively justify an arbitrary choice. When evidence is insufficient, write `proposed`, preserve alternatives, and ask one decision-focused question.

## Consistency review

Before transition confirm:

- system boundary matches use-case scope;
- every important actor/external system appears in context;
- every priority scenario has an ownership path;
- data ownership and trust crossings are visible where material;
- failure and recovery responsibilities exist;
- diagrams, responsibility tables, and prose agree;
- material choices have ADRs with real consequences;
- unknowns and proposed decisions are labelled;
- no diagram implies stakeholder agreement that has not occurred.

Use Mermaid source plus prose/table fallback so the model remains reviewable without rendering. Update prior artifacts if architecture analysis exposes a behavior or goal contradiction.

When architecture-driving behavior is explained and material decisions are either explicit or visibly open, add `architecture` to `completed_phases`, set `current_phase` to `review`, and synchronize architecture and ADR paths in `snapshot_paths`.

Next transition: `alignment:review-alignment`.
