# Epistemic Alignment Plugin Package — Design Specification

**Date:** 2026-08-27

**Status:** Approved in conversation for specification

**Initial platform:** Codex desktop

**Future adapters:** Claude, OpenCode, Qwen Code

## 1. Purpose

Build a plugin package, modeled after Superpowers, that establishes a shared and auditable understanding of a complex software initiative before implementation planning begins.

The package guides an agent and its human stakeholders through:

1. domain and stakeholder discovery;
2. Cockburn-style use cases;
3. BDD scenarios;
4. C4 architecture modeling and architectural decisions;
5. a stakeholder-facing review site;
6. a strict human approval gate;
7. a traceable handoff to Superpowers.

The first complete implementation targets Codex and creates a ChatGPT Sites-compatible review project. The methodology and canonical artifacts remain independent of any agent harness so later adapters can render the same package as a Claude Artifact or local site in OpenCode and Qwen Code.

## 2. Design principles

- **Skills, not an orchestration runtime.** The package is a set of composable skills plus deterministic validation helpers. It does not replace the host agent loop.
- **Canonical data before presentation.** Markdown, Gherkin, Mermaid, YAML, and JSON are the source of truth. Sites and Artifacts are derived views.
- **Human-only approval.** An agent may recommend approval readiness but may never approve its own output.
- **Explicit epistemic status.** Facts, stakeholder statements, agent inferences, assumptions, and unknowns are distinguishable.
- **End-to-end traceability.** Goals trace to stakeholders, use cases, BDD scenarios, architecture elements, and decisions.
- **Revision invalidates approval.** Approval is tied to the exact semantic content that was reviewed.
- **Restartability.** A failed phase resumes from valid artifacts rather than regenerating the whole package.
- **Progressive depth.** Complex initiatives receive the full workflow; bounded work may skip it with an explicit recorded rationale.

## 3. Scope

### 3.1 Version-one scope

- A Codex plugin manifest and installable plugin package.
- A suite of alignment skills with one primary entry skill.
- Templates and guidance for discovery, Cockburn use cases, BDD, C4, ADRs, review, approval, and Superpowers handoff.
- A deterministic command-line validator and content-hash helper.
- A Codex Sites renderer skill that creates a review site project from canonical artifacts.
- Fixtures, validator tests, scenario evals, and a clean-install smoke test.
- Documentation of the adapter contract for Claude, OpenCode, and Qwen Code.

### 3.2 Non-goals for version one

- A new agent runtime, durable workflow engine, or replacement for Codex/Superpowers.
- A hosted collaboration backend, user accounts, or a comment database.
- Approval buttons that persist state directly from the site.
- Automatic publication without explicit human consent.
- Full production implementations of the Claude, OpenCode, or Qwen Code adapters.
- Automatic interception of every prompt. Host skill selection cannot guarantee a global pre-hook.

## 4. Package architecture

The plugin is a method layer with three parts:

1. **Skill suite** — conducts the alignment workflow.
2. **Artifact contract and validator** — stores and verifies portable project understanding.
3. **Renderer adapters** — present the same artifacts in a platform-appropriate form.

The primary skill namespace is `alignment`. The main entry point is `alignment:align-project`.

### 4.1 Skill responsibilities

| Skill | Responsibility |
| --- | --- |
| `alignment:align-project` | Qualify the task, orchestrate phases, preserve state, and enforce the gate. |
| `alignment:discover-domain` | Identify goals, stakeholders, vocabulary, constraints, evidence, assumptions, and open questions. |
| `alignment:write-use-cases` | Produce Cockburn-style use cases with actors, guarantees, main success scenarios, and extensions. |
| `alignment:specify-behavior` | Produce BDD/Gherkin scenarios linked to use cases and goals. |
| `alignment:model-architecture` | Produce C4 models and ADRs linked to required behavior. |
| `alignment:verify-alignment` | Run deterministic checks and semantic cross-checks; report exact blockers. |
| `alignment:build-review` | Select the host adapter and build a stakeholder-facing review view. |
| `alignment:approve-handoff` | Record a human decision, verify its content hash, and create the Superpowers handoff. |

Each skill has one clear input/output contract and may be used independently. `align-project` is the normal front door for a new complex initiative.

### 4.2 Relationship to Superpowers

Alignment owns the shared understanding of the problem. Superpowers owns implementation design, planning, execution, debugging, and review.

The handoff boundary is:

```text
request
  -> alignment:align-project
  -> approved handoff.md
  -> superpowers:brainstorming
  -> superpowers:writing-plans
  -> implementation workflow
```

The alignment package does not duplicate Superpowers implementation planning. It provides an approved problem model that Superpowers must treat as its starting context.

Superpowers is an integration dependency for the final handoff test, not for authoring or reviewing alignment artifacts. If it is unavailable, the package may complete review and generate a verified `handoff.md`, but it must report that delivery is pending rather than claiming the handoff was consumed.

Because Codex plugins cannot guarantee that one skill intercepts all project requests, the package uses both:

- a broad and precise description that encourages automatic selection for greenfield, ambiguous, architectural, or stakeholder-heavy work; and
- an explicit `alignment:align-project` entry point users can request directly.

## 5. Workflow

The workflow is a resumable state machine:

```text
qualify -> discover -> use_cases -> behavior -> architecture
     -> cross_check -> review -> decision -> handoff
                         ^           |
                         +-- revise -+
```

### 5.1 Qualification

The full process is required when any of these conditions holds:

- a new product, service, or substantial subsystem is being created;
- the work changes architecture or public interfaces;
- requirements are ambiguous or contradictory;
- multiple stakeholder perspectives affect success;
- failure would cause material time, money, safety, privacy, or operational risk.

A human may force alignment for any task. A bounded task may skip alignment only when the agent records a short rationale; skipping creates no approval or handoff artifact.

### 5.2 Discovery

The agent asks one material question at a time and may inspect the existing repository and approved external sources. It separates:

- verified repository or source facts;
- direct stakeholder statements;
- preferences and desired outcomes;
- constraints;
- agent inferences;
- assumptions requiring confirmation;
- open questions.

Discovery ends when the charter, stakeholder map, glossary, constraints, assumptions, and open questions are internally consistent enough to model use cases. Unresolved critical questions may remain visible but block final approval.

### 5.3 Cockburn use cases

Each use case includes:

- stable ID and title;
- scope and level;
- primary and supporting actors;
- stakeholder interests;
- preconditions;
- minimal and success guarantees;
- trigger;
- numbered main success scenario;
- numbered extensions referring to main-flow steps;
- relevant business rules, data, frequency, and open issues;
- links to goals and evidence.

The agent must model user intent and system responsibility, not UI click sequences unless the UI behavior is itself contractually relevant.

### 5.4 BDD

BDD features and scenarios express externally observable behavior. Every priority use case has at least one happy-path scenario and scenarios for material extensions or failure modes. Each feature or scenario carries tags that link it to use-case and goal IDs.

The agent must not invent acceptance criteria silently. Inferred criteria are marked as proposed assumptions until confirmed.

### 5.5 C4 and decisions

The architecture phase produces the minimum useful C4 depth:

- System Context is mandatory.
- Container is mandatory for software systems with more than one deployable or data store.
- Component diagrams are created only for containers whose internal structure materially affects an important behavior or decision.
- Code diagrams are outside version-one scope.

Architecture elements link to behaviors they enable. Material choices are captured as ADRs with context, decision, alternatives, consequences, evidence, and affected IDs.

### 5.6 Cross-check and review

Cross-checking combines:

- deterministic structural validation;
- semantic review by the agent;
- a stakeholder-facing review site.

The agent reports blockers and warnings separately. It corrects local structural problems without regenerating unrelated valid artifacts. Changes proposed by the agent retain `proposed` status until a human confirms them.

### 5.7 Decision and handoff

The only valid human decisions are:

- `approved`;
- `changes_requested`;
- `rejected`.

Only `approved` can unlock a handoff. `changes_requested` loops to the relevant phase. `rejected` closes the current alignment attempt without a handoff.

## 6. Canonical artifact contract

Target projects store source-of-truth artifacts under `alignment/`:

```text
alignment/
├── manifest.yaml
├── charter.md
├── stakeholders.md
├── glossary.md
├── assumptions.md
├── open-questions.md
├── use-cases/
│   └── UC-*.md
├── features/
│   └── *.feature
├── architecture/
│   ├── context.md
│   ├── containers.md
│   └── components.md
├── decisions/
│   └── ADR-*.md
├── review-state.json
└── handoff.md
```

`handoff.md` is absent until an approved decision passes validation. Generated presentation sources live outside the canonical directory, under `alignment-review/`, and may be deleted and rebuilt.

### 6.1 Manifest

`manifest.yaml` records:

- schema version;
- project identifier and title;
- current phase;
- completed phases and artifact paths;
- adapter and renderer status;
- last successful validation;
- the canonical content hash when a review is issued.

The manifest describes progress but does not override the actual artifact contents.

### 6.2 Stable IDs

The initial ID families are:

- `GOAL-nnn` — goals and measurable outcomes;
- `STK-nnn` — stakeholders and actors;
- `ASM-nnn` — assumptions;
- `Q-nnn` — open questions;
- `UC-nnn` — use cases;
- `SCN-nnn` — BDD scenarios;
- `SYS-nnn`, `CTR-nnn`, `CMP-nnn` — C4 elements;
- `ADR-nnn` — decisions.

IDs are never silently reused after deletion. Superseded entities retain their ID and status so references and prior reviews remain interpretable.

### 6.3 Epistemic metadata

Every material claim or entity exposes:

- `source_kind`: `human`, `repository`, `external`, or `agent_inference`;
- `source_ref`: a file, conversation reference, source URL, or stakeholder ID;
- `status`: `proposed`, `confirmed`, `rejected`, or `superseded`;
- `confidence`: `high`, `medium`, or `low`;
- `evidence`: zero or more references supporting the claim.

An `agent_inference` cannot become `confirmed` without human confirmation or stronger authoritative evidence.

Markdown artifacts encode entity metadata in YAML front matter or explicitly delimited YAML records defined by the shipped templates. Gherkin artifacts encode stable links as tags and place claim metadata in a machine-readable adjacent comment block. The schema and templates define one representation for each artifact type; free-form prose alone never satisfies a required machine-readable field.

### 6.4 Traceability invariant

The required trace is:

```text
Goal -> Stakeholder -> Use Case -> BDD Scenario -> C4 Element -> ADR
```

Not every chain requires an ADR, but every priority goal must be represented by a stakeholder need and use case; every priority use case must have BDD coverage; and every scenario that depends on software responsibility must map to at least one owning C4 element.

The validator reports orphaned, broken, duplicated, and invalid references. It also calculates coverage summaries for the review site.

## 7. Approval model

### 7.1 Readiness requirements

Approval is valid only when:

- no critical open question remains;
- no critical assumption remains merely proposed;
- every priority goal and use case satisfies the traceability invariant;
- required BDD coverage exists;
- required C4 levels and relevant ADRs exist;
- deterministic validation passes;
- the review site or an explicitly recorded equivalent review view was presented;
- a human explicitly approves the reviewed content hash.

Warnings may remain if the human acknowledges them in the decision record.

### 7.2 Content hash

The helper computes a deterministic SHA-256 hash from normalized canonical artifacts. It excludes:

- all of `review-state.json`, because validation, presentation, and decisions are review outputs rather than reviewed problem-model content;
- generated `handoff.md`;
- generated presentation files;
- timestamps and other declared non-semantic manifest fields.

Normalization uses stable path ordering, UTF-8, LF line endings, and a documented representation for semantic manifest fields. The review record stores the algorithm version and exact hash.

Any semantic change after approval produces a different hash and invalidates approval. The workflow returns to review; a stale approval can never create a handoff.

### 7.3 Review state

`review-state.json` contains:

- validation status, blockers, and warnings;
- renderer and presentation status;
- issued review hash and issuance time;
- human decision, reviewer identity label, decision time, and acknowledged warnings;
- decision provenance indicating that it came from a human interaction;
- the approval hash verified during handoff.

The agent may write readiness results and transcribe an explicit human decision. It may not synthesize an approval decision.

### 7.4 Trust boundary

Version one enforces human-only approval as an agent workflow invariant, not as cryptographic identity authentication. The reviewer identity is a human-supplied label, and the approval skill may transcribe `approved` only from an explicit human message in the current host interaction. The deterministic helper verifies schema, decision provenance fields, readiness, and content-hash equality; it cannot prove that an arbitrary file edit was authored by a human. Tests therefore cover both deterministic tamper/staleness checks and behavioral evals that ensure the agent never fabricates approval. Cryptographically signed or server-authenticated approvals remain outside version-one scope.

## 8. Codex review site

The Codex renderer turns `alignment/` into a ChatGPT Sites-compatible project under `alignment-review/site/`. The generated project contains the Sites hosting configuration required by the current Codex desktop workflow.

The review experience contains seven views:

1. executive summary, goals, scope, and success measures;
2. stakeholder map and glossary;
3. Cockburn use cases;
4. BDD behavior and coverage;
5. navigable C4 diagrams and owning responsibilities;
6. ADRs, assumptions, open questions, contradictions, and risks;
7. readiness and approval dashboard.

Every summary links back to canonical IDs. Low-confidence or proposed material is visibly distinct from confirmed material. Blockers cannot be hidden behind a generic readiness score.

The version-one site is presentational. Review discussion and approval occur in the Codex conversation and are transcribed to `review-state.json` by the approval skill.

The renderer must support draft generation and visual inspection without publication. Publishing or updating a hosted Site requires explicit human consent because it changes external state. A publishing failure does not affect canonical artifacts and leaves presentation status incomplete.

## 9. Adapter contract

Every renderer adapter receives:

- the canonical `alignment/` directory;
- validated traceability and coverage output;
- the issued review hash;
- platform capabilities and publication policy.

It returns:

- renderer identity and version;
- generated artifact location or platform reference;
- generation and presentation status;
- the exact review hash rendered;
- warnings or failures.

Planned adapters:

- **Codex:** ChatGPT Sites-compatible project and Sites workflow.
- **Claude:** a Claude Artifact rendering the same review model.
- **OpenCode:** local static review site plus a local preview command.
- **Qwen Code:** local static review site plus a local preview command.

The OpenCode and Qwen Code adapters may share the static renderer but expose host-specific installation instructions and invocation metadata.

## 10. Failure handling and recovery

- Each completed phase is recorded in the manifest with its artifacts and validation result.
- A phase is complete only when its required files parse and pass phase-specific structural checks.
- On restart, the orchestrator reads the manifest and validates referenced artifacts before resuming.
- Missing or corrupt artifacts roll back only the affected phase and dependent phases.
- Broken cross-references produce actionable diagnostics with file, entity ID, and expected correction.
- Semantic contradictions are preserved as explicit blockers rather than silently resolved by the agent.
- A renderer failure is isolated from the canonical model.
- A stale review hash forces a new review.
- Validator crashes or unsupported schema versions fail closed: no approval or handoff is produced.

## 11. Deterministic helper

The package ships a dependency-light helper CLI for operations that should not depend on model judgment:

- initialize the canonical directory from templates;
- validate schema and references;
- calculate coverage;
- calculate and verify the canonical content hash;
- check approval readiness;
- generate the deterministic portion of `handoff.md`.

The helper does not orchestrate the agent or author requirements. It makes invariants reproducible across supported harnesses.

## 12. Testing strategy

### 12.1 Validator tests

Automated tests cover:

- valid minimal and full artifact packages;
- malformed manifests and unsupported schema versions;
- duplicate, missing, broken, and superseded IDs;
- goal/use-case/BDD/C4 coverage rules;
- critical assumptions and questions;
- deterministic hashing across path ordering and line endings;
- approval invalidation after semantic changes;
- rejection of stale, malformed, or explicitly agent-provenance approvals;
- recovery boundaries for corrupt artifacts.

### 12.2 Skill scenario evals

Repeatable fixtures evaluate skill behavior for:

- a greenfield SaaS product;
- a substantial change in an existing repository;
- conflicting stakeholder requirements;
- a critical unknown that must block approval;
- a bounded task that may legitimately skip alignment;
- a post-approval change that must invalidate the handoff.

Evals inspect both required artifacts and forbidden behavior, especially silent inference confirmation and agent self-approval.

### 12.3 Site verification

The generated Codex review site receives:

- a production build check;
- link and canonical-ID integrity checks;
- representative desktop and narrow-viewport visual inspection;
- accessibility checks for navigation, contrast, headings, and status communication;
- a check that blockers, provenance, and uncertainty remain visible.

### 12.4 End-to-end smoke test

A clean Codex installation must demonstrate:

```text
complex request
  -> alignment skill selected or explicitly invoked
  -> canonical artifacts created
  -> deterministic validation passes
  -> review site generated and inspected
  -> explicit human approval recorded
  -> content hash verified
  -> handoff.md generated
  -> Superpowers receives the handoff
```

## 13. Release criteria

The Codex-first version is ready when:

- the plugin installs from a clean local or marketplace source;
- all documented skills are discoverable and internally linked;
- artifact initialization and validation work without undeclared dependencies;
- all validator tests pass;
- skill scenario evals demonstrate the required gates;
- the example review site builds and passes visual inspection;
- the end-to-end smoke test reaches Superpowers only after a verified human approval;
- installation, usage, recovery, and removal are documented;
- the adapter contract and road map for Claude, OpenCode, and Qwen Code are included.

## 14. Delivery sequence

1. Establish the plugin manifest, repository conventions, and canonical templates.
2. Implement the deterministic helper test-first.
3. Implement and evaluate the core alignment skills.
4. Implement the Codex Sites renderer and verify its output visually.
5. Run a clean-install end-to-end smoke test.
6. Document the cross-harness adapter contract and future adapter work.
7. Prepare the repository for GitHub publication.

Full Claude, OpenCode, and Qwen Code adapters follow as separate implementation cycles after the Codex-first release proves the method and artifact contract.
