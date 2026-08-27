---
name: write-use-cases
description: Use when discovered stakeholder goals and constraints need human-readable Cockburn use cases before behavior examples are specified.
---

# Write Use Cases

Express a stakeholder goal as responsibilities, guarantees, and recoverable paths.

## Contract

Input: discovery dossier files and material stakeholder goals. Output: `alignment/use-cases/UC-*.md` files linked to their discovery evidence. Read [the Cockburn recipe](../shared/references/cockburn.md) and [dossier contract](../shared/references/artifact-contract.md).

1. Read existing discovery and use-case files. Continue an incomplete use case before creating another.
2. Select one material actor goal. If its intent, guarantee, or conflict is unclear, ask one material question and record the answer in discovery first.
3. Create or revise one Cockburn file using every template slot: scope, level, actor, interests, conditions, guarantees, trigger, numbered success scenario, extensions, rules, frequency, and issues.
4. Link constraints, assumptions, contradictions, and open questions by readable source reference. Treat unresolved conditions as extensions or open issues.
5. Keep each step at an actor-intent or system-responsibility level; make failure recovery observable.

Do not substitute screen choreography for the goal model unless the interface is contractual. Next transition: `alignment:specify-behavior`.
