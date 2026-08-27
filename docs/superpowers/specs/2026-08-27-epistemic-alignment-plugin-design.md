# Epistemic Alignment Plugin Package — Design Specification

**Date:** 2026-08-27

**Status:** Approved, revised to thin-gate architecture

**Initial platform:** Codex desktop

**Future adapters:** Claude, OpenCode, Qwen Code

## 1. Purpose

Build a Superpowers-style plugin package that helps an agent and its stakeholders reach a shared, inspectable understanding of a complex software initiative before implementation planning begins.

The package guides them through:

1. domain and stakeholder discovery;
2. Cockburn-style use cases;
3. BDD scenarios;
4. C4 architecture modeling and architectural decisions;
5. a stakeholder-facing review site;
6. explicit human approval of the reviewed snapshot;
7. a hash-verified handoff to Superpowers.

The first complete implementation targets Codex and creates a ChatGPT Sites review project. The method and documents remain portable so Claude can render an Artifact and OpenCode/Qwen Code can render a local site later.

## 2. Core decision: skills plus a thin gate

The plugin is primarily a skill package. Model judgment and human review own semantics. A small deterministic helper owns only operations that computers can perform without pretending to understand the domain:

- initialize the document set;
- hash the reviewed files;
- record an explicit human decision;
- reject stale or missing approval;
- create a handoff carrying the approved hash.

The helper is not a semantic validator. It does not decide whether a use case is correct, calculate BDD completeness, parse C4 ownership, require metadata on every claim, or certify stakeholder agreement. Those tasks remain visible skill and human-review responsibilities.

This boundary follows the successful Superpowers model: prompts and independent review enforce methodology; deterministic scripts support process mechanics without becoming a second agent runtime.

## 3. Design principles

- **Skills, not a workflow runtime.** The host agent remains responsible for execution and interaction.
- **Documents before presentation.** Markdown, Gherkin, Mermaid, and ADRs are the source of truth; Site/Artifact/HTML are derived views.
- **Human-only approval.** The agent can assess readiness but cannot approve its own work.
- **Visible uncertainty.** Facts, stakeholder statements, assumptions, contradictions, and open questions are visibly distinct in the documents and review.
- **Traceable enough for humans.** Stable IDs and cross-links are recommended and reviewed, but no bespoke compiler claims semantic correctness.
- **Snapshot integrity.** Approval applies to the exact file snapshot shown to the stakeholder; any included-file change invalidates it.
- **Restartability through files.** Skills inspect the existing dossier and continue from the first incomplete phase.
- **Progressive depth.** Complex work receives the full process; bounded work can skip it with a written rationale.

## 4. Version-one scope

### Included

- An installable Codex plugin manifest.
- Eight focused skills with `alignment:align-project` as the front door.
- Portable templates and method references for discovery, Cockburn, BDD, C4, ADR, review, approval, and handoff.
- A Python 3.9 standard-library helper for initialization, snapshot hashing, decision recording, stale-approval checks, and handoff generation.
- A Codex Sites skill and template for stakeholder review.
- Illustrative scenario examples covering the intended workflow and prohibited behavior for manual inspection.
- Documentation of a common adapter contract for Claude, OpenCode, and Qwen Code.

### Excluded

- A semantic parser or requirements compiler.
- Machine certification of requirement quality, BDD coverage, C4 correctness, or stakeholder consensus.
- A machine-assertion corpus or evaluator that treats scenario examples as a release gate.
- Mandatory machine-readable metadata on every statement.
- A durable orchestration runtime or replacement for Codex/Superpowers.
- A hosted comment backend, user accounts, or interactive approval persistence inside the Site.
- Automatic Site publication without explicit human consent.
- Production Claude, OpenCode, or Qwen Code adapters in the Codex-first release.
- Guaranteed interception of every prompt; host skill selection has no global pre-hook guarantee.

## 5. Package architecture

The package has three layers:

1. **Method skills** author and review the dossier.
2. **Thin snapshot gate** protects approval integrity.
3. **Renderer adapters** present the dossier in the host's native form.

### 5.1 Skills

| Skill | Responsibility |
| --- | --- |
| `alignment:align-project` | Qualify work, sequence phases, resume from existing files, and enforce the human gate. |
| `alignment:discover-domain` | Establish goals, stakeholders, vocabulary, constraints, assumptions, contradictions, and open questions. |
| `alignment:write-use-cases` | Write Cockburn-style use cases grounded in discovery. |
| `alignment:specify-behavior` | Write BDD/Gherkin examples tied back to use cases in human-readable form. |
| `alignment:model-architecture` | Write C4 diagrams and ADRs that explain how required behavior will be supported. |
| `alignment:review-alignment` | Perform a semantic cross-review and make gaps/contradictions visible without claiming machine proof. |
| `alignment:build-review` | Build the appropriate Site, Artifact, or local review presentation. |
| `alignment:approve-handoff` | Snapshot reviewed files, transcribe an explicit human decision, verify freshness, and create the Superpowers handoff. |

Each skill has one input/output boundary and can be invoked independently. `align-project` is the normal entry for greenfield, architectural, ambiguous, or stakeholder-heavy work.

### 5.2 Relationship to Superpowers

Alignment owns shared understanding of the problem. Superpowers owns implementation design, planning, TDD, debugging, and review.

```text
request
  -> alignment:align-project
  -> human-approved handoff.md
  -> superpowers:brainstorming
  -> superpowers:writing-plans
  -> implementation workflow
```

Superpowers is needed for the final integration handoff, but not for authoring or reviewing the alignment dossier. If Superpowers is unavailable, the plugin may create a verified `handoff.md` and must report delivery as pending.

## 6. Workflow

```text
qualify -> discover -> use_cases -> behavior -> architecture
     -> semantic_review -> presentation -> decision -> handoff
                                ^             |
                                +--- revise --+
```

### 6.1 Qualification

The full process is appropriate when any of these holds:

- a new product, service, or substantial subsystem is being created;
- architecture or public interfaces change;
- requirements are ambiguous or contradictory;
- several stakeholder perspectives affect success;
- failure carries material time, financial, safety, privacy, or operational risk.

A human can force alignment for any work. A bounded task may skip it only with a short recorded rationale; skipping creates neither approval nor handoff.

### 6.2 Discovery

The agent asks one material question at a time and may inspect the repository and approved sources. It separates verified facts, stakeholder statements, desired outcomes, constraints, agent inferences, assumptions, contradictions, and open questions.

### 6.3 Cockburn use cases

Each use case includes scope, level, actors, stakeholder interests, preconditions, minimal and success guarantees, trigger, numbered main success scenario, extensions, business rules, frequency, and open issues. It models intent and responsibility rather than UI clicks unless UI behavior is itself contractual.

### 6.4 BDD

BDD scenarios describe observable examples for priority use cases and material extensions. The dossier uses readable IDs/tags to make relationships navigable. Inferred acceptance criteria remain clearly proposed until a human confirms them.

### 6.5 C4 and decisions

System Context is expected for software systems. Container diagrams are expected when multiple deployables or stores matter. Component diagrams are created only where internal structure materially affects important behavior or a decision. Material choices become ADRs.

### 6.6 Semantic review

The review skill rereads the dossier as a skeptical reviewer and reports:

- stakeholder goals without a convincing use case;
- important use-case paths without concrete examples;
- architecture elements with no explained responsibility;
- decisions with unexplored consequences;
- conflicting statements;
- assumptions presented as facts;
- critical open questions.

These are review findings, not compiler diagnostics. The agent records them in the dossier and review summary, and a human decides whether they are resolved or acceptable.

### 6.7 Presentation and decision

The renderer presents both understanding and uncertainty. The stakeholder responds `approved`, `changes_requested`, or `rejected` in the host conversation. The stakeholder does not need to repeat or copy the digest; the agent binds that explicit current reply internally to the current issued digest when invoking the helper CLI. Only an explicit human message in the current interaction can be transcribed as approval, and it must never be bound to a superseded issuance.

`changes_requested` returns to the relevant phase. `rejected` closes the attempt without a handoff. `approved` unlocks a handoff only while the reviewed snapshot remains current.

## 7. Dossier contract

Target projects use this default structure:

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
├── review.md
├── review-state.json
└── handoff.md
```

`handoff.md` is absent until the approval gate passes. `review.md` is the human-readable semantic review. Generated presentation files live under `alignment-review/` and can be rebuilt.

`manifest.yaml` records project identity, current phase, included snapshot paths, and renderer state. It remains JSON-compatible YAML so the dependency-free helper can read it. The helper verifies only manifest shape and safe file paths; it does not parse document semantics.

Documents use human-readable stable IDs such as `GOAL-001`, `UC-001`, `SCN-001`, and `ADR-001` when useful. The skills preserve links and highlight provenance/uncertainty in prose or tables. These conventions support review and navigation without turning Markdown into a database schema.

## 8. Thin snapshot gate

### 8.1 Snapshot hash

The helper computes `sha256-v1` over the included dossier paths declared in the manifest. It:

- rejects missing files, paths outside `alignment/`, duplicates, symlinks escaping the dossier, and invalid UTF-8 text;
- uses sorted POSIX paths, UTF-8, and LF normalization;
- excludes `review-state.json`, generated `handoff.md`, presentation output, timestamps, renderer state, and stored hashes;
- does not parse or judge document contents.

A formatting change in an included document conservatively changes the hash. This is intentional: the approved snapshot is exactly what was presented.

### 8.2 Review state

`review-state.json` stores:

- snapshot algorithm and issued hash;
- included paths;
- presentation adapter, status, location/reference, and rendered hash;
- human decision, reviewer label, provenance, decision time, and acknowledged review findings;
- handoff verification time, approved snapshot hash, and exact handoff-content
  SHA-256.

The reviewer label is not authenticated identity. Version one enforces human-only approval as an agent workflow rule, not a cryptographic signature.

### 8.3 Gate rules

The helper can create `handoff.md` only when:

- the current snapshot hash equals the issued, rendered, and approved hashes;
- presentation status is `presented` or `published`;
- decision is `approved`;
- provenance is `human-message`;
- the recorded decision belongs to the current review issuance;
- the review state and manifest use supported schema versions.

The helper does not infer whether semantic findings are resolved. The approval skill must show `review.md` findings to the human and transcribe the explicit decision. Scenario examples illustrate the protocol; deterministic helper tests cover the mechanical approval boundary.

When `handoff.md` exists, readiness also requires a complete handoff record and
an exact SHA-256 match to the helper-generated bytes at that regular,
non-symlink path. Missing or malformed records, missing files, symlinks,
non-regular files, byte mismatches, and unresolved handoff transactions fail
closed. Approval before initial handoff generation remains ready only while
both the handoff file and record are absent.

## 9. Codex review Site

The Codex adapter builds a ChatGPT Sites-compatible project under `alignment-review/site/`. The build-review skill reads the dossier and creates seven views:

1. executive summary and goals;
2. stakeholder map and glossary;
3. Cockburn use cases;
4. BDD examples;
5. C4 diagrams and responsibilities;
6. ADRs, assumptions, contradictions, questions, and risks;
7. semantic-review findings, snapshot hash, and decision readiness.

Every summary links back to dossier files/IDs. Proposed, uncertain, or conflicting material must remain visually distinct. There is no approval button in version one; the host conversation is the decision channel.

Draft generation and visual inspection do not publish. Hosting or updating a Site requires explicit human consent. Publishing failure cannot alter the dossier or manufacture presentation status.

## 10. Adapter contract

Every renderer receives the dossier directory, included-path list, issued snapshot hash, semantic review, and platform capabilities. It returns adapter/version, generated location or reference, status, rendered hash, and warnings.

- **Codex:** ChatGPT Sites project and Sites workflow.
- **Claude:** Claude Artifact showing the same dossier and findings.
- **OpenCode:** local static site and explicit preview command.
- **Qwen Code:** the same local renderer with Qwen extension/skill metadata.

The local renderers can share implementation later; their host installation and invocation metadata remain separate.

## 11. Failure handling

- Skills resume by inspecting existing files and `manifest.yaml` rather than relying on conversation memory.
- The initializer refuses to overwrite an existing dossier.
- Missing or unsafe included paths fail snapshot creation with actionable file-level errors.
- A document change after review makes approval stale and blocks handoff.
- A Site failure leaves the dossier untouched and presentation incomplete.
- Unsupported manifest/review-state versions fail closed.
- Semantic contradictions remain visible findings; the helper never silently resolves them.

## 12. Testing

### Helper tests

- initialization and overwrite refusal;
- safe manifest path handling;
- deterministic hashing across path order and line endings;
- snapshot changes after included-file edits;
- exclusion of decision/presentation state and generated files;
- rejection of missing, duplicate, escaping, or unsafe paths;
- rejection of stale, malformed, non-human-provenance, or unpresented approvals;
- successful handoff with equal issued/rendered/approved/current hashes.

### Skill scenario examples

- greenfield project;
- existing repository change;
- conflicting stakeholder requirements;
- critical unknown retained in review;
- bounded task skipped with rationale;
- post-approval edit invalidating handoff;
- attempted agent self-approval rejected by the skill protocol.

### Site verification

- production build and link checks;
- desktop and narrow-viewport visual inspection;
- keyboard, headings, contrast, and labeled-status accessibility;
- visibility of uncertainty, contradictions, review findings, and snapshot hash.

### End-to-end smoke test

```text
complex request
  -> alignment skill
  -> discovery + Cockburn + BDD + C4
  -> semantic review
  -> Site generated and presented
  -> explicit human approval of snapshot hash
  -> unchanged snapshot verified
  -> handoff.md generated
  -> Superpowers consumes handoff
```

## 13. Release criteria

The Codex-first release is ready when:

- the plugin installs cleanly and all eight skills are discoverable;
- the helper works on Python 3.9 without third-party runtime dependencies;
- no semantic parser/validator is present;
- helper tests prove snapshot and approval integrity;
- illustrative scenario examples document the method and prohibited behaviors for manual inspection;
- the example Site builds and passes visual/accessibility inspection;
- a clean-install E2E reaches Superpowers only after an unchanged, human-approved snapshot;
- installation, usage, recovery, trust boundary, and removal are documented;
- the adapter contract and concrete Claude/OpenCode/Qwen Code road maps are included.

## 14. Delivery sequence

1. Keep the verified plugin skeleton and safe dossier initialization.
2. Implement the dependency-free snapshot and approval helper test-first.
3. Author the alignment skill suite and record illustrative scenarios.
4. Build and visually verify the Codex Site adapter.
5. Manually inspect scenario examples and run a clean-install E2E.
6. Document cross-harness adapters and prepare the repository for GitHub publication.

Production Claude, OpenCode, and Qwen Code adapters remain separate implementation cycles after the Codex-first release proves the method and thin-gate contract.
