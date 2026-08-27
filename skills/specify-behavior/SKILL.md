---
name: specify-behavior
description: Use when priority use cases or material extensions need observable acceptance examples before architecture decisions are modeled.
---

# Specify Behavior

Turn an agreed goal path into concrete, reviewable examples.

## Contract

Input: `alignment/use-cases/`, discovery context, and confirmed or proposed criteria. Output: linked `alignment/features/*.feature` files. Read [the BDD recipe](../shared/references/bdd.md).

1. Inspect existing feature files and use cases; continue the first material path without an example.
2. Choose one main success path or material extension. Ask one question only when its observable starting state or result remains unknown.
3. Write a Gherkin feature with `alignment-meta`, stable scenario/use-case tags, one rule where applicable, and Given/When/Then language describing externally visible behavior.
4. Include the boundary, failure, or recovery case when it changes the stakeholder outcome. Link assumptions and open questions instead of guessing them away.
5. Mark proposed criteria as proposed until a human confirms them.

Do not write APIs, internal algorithms, or test-framework mechanics as acceptance behavior. Next transition: `alignment:model-architecture`.
