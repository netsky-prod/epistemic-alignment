# Epistemic Alignment v0.1.0 completion audit

Audit date: 2026-08-28

Round-3 baseline: `def9143a1ead48d388e3bb4ef69cf56002f40ab8`

Authority: the revised [thin-gate design](../../docs/superpowers/specs/2026-08-27-epistemic-alignment-plugin-design.md), not the superseded semantic-validator design.
Allowed statuses: `proven`, `contradicted`, `missing`. Any status other than
`proven` blocks release.

The seven cases, five captured semantic runs, and two case-only helper
walkthroughs are non-authoritative examples for human inspection. Their
presence is evidence of the documented example deliverable, not semantic proof
or a release gate. Hashes below are internal integrity metadata; a normal human
approval reply does not require copying a digest.

## Version-one scope

| Requirement | Status | Concrete evidence |
| --- | --- | --- |
| Installable Codex plugin manifest | proven | [manifest](../../.codex-plugin/plugin.json); `tests.test_plugin_package`; pinned plugin-creator validation command in the [README](../../README.md) |
| Exactly eight focused skills with `alignment:align-project` as front door | proven | [skills](../../skills); `tests.test_skills.SkillTests.test_exact_skill_set`; clean-install skill inventory in `tests.test_release` |
| Each skill declares exactly one input/output boundary | proven | Boundary regression across all eight skills in [skill tests](../../tests/test_skills.py) |
| Each skill can be invoked independently without the front door or prior conversation | proven | All eight interfaces are explicit in [skill tests](../../tests/test_skills.py); the required real fresh-context `alignment:specify-behavior` [input/result exercise](skill-invocations/specify-behavior), [transcript](skill-invocations/specify-behavior/transcript.md), bound [provenance](skill-invocations/specify-behavior/provenance.json), and mechanical replay in [release tests](../../tests/test_release.py) demonstrate the direct mechanics |
| Portable templates/references for discovery, Cockburn, BDD, C4, ADR, review, approval, and handoff | proven | [templates](../../templates/alignment), [references](../../references), and `tests.test_skills.SkillTests.test_shared_method_references_exist` |
| Python 3.9 standard-library helper for init, snapshot, decision, stale checks, and handoff | proven | [launcher](../../scripts/alignment), [source](../../src/epistemic_alignment), [installation requirements](../../docs/installation.md), and the full Python suite |
| Codex Sites skill and stakeholder-review template | proven | [build-review skill](../../skills/build-review/SKILL.md), [Site template](../../adapters/codex-site/template), and adapter Site suite |
| Illustrative intended/prohibited workflow examples | proven | [eval README](../../evals/README.md), [seven cases](../../evals/cases), and [five captured runs](../evals/runs) |
| Common contract and Claude/OpenCode/Qwen Code documentation | proven | [contract](../../adapters/adapter-contract.md) and host road maps under [adapters](../../adapters) |
| No semantic parser or requirements compiler | proven | [thin-boundary tests](../../tests/test_thin_boundary.py) and the prescribed negative `rg` audit |
| No machine certification of requirements, BDD, C4, or consensus | proven | [trust model](../../docs/trust-model.md), [semantic-review skill](../../skills/review-alignment/SKILL.md), and no production semantic validator in the negative audit |
| No machine-assertion eval corpus or evaluator release gate | proven | [eval README](../../evals/README.md); `scripts/check-evals` is absent; release commands contain no checker invocation |
| No mandatory metadata on every statement | proven | [artifact contract](../../references/artifact-contract.md) uses human-readable conventions and a file-membership invariant only |
| No durable orchestration runtime or Superpowers replacement | proven | [align-project skill](../../skills/align-project/SKILL.md), [trust model](../../docs/trust-model.md), and helper source limited to deterministic mechanics |
| No hosted comments, users, or Site approval persistence | proven | [hosting config](../../adapters/codex-site/template/.openai/hosting.json), `tests.test_codex_site`, and Site rendered suite |
| No automatic Site publication | proven | [build-review skill](../../skills/build-review/SKILL.md), [usage guide](../../docs/usage.md), and `publication_performed: false` in [E2E evidence](e2e.json) |
| No production Claude/OpenCode/Qwen Code adapters | proven | The three files under [adapters](../../adapters) explicitly identify themselves as road maps; no host implementation is shipped |
| No claim of global prompt interception | proven | [trust model](../../docs/trust-model.md) records the host-selection limitation |

## Workflow phases

| Phase/rule | Status | Concrete evidence |
| --- | --- | --- |
| Qualification for substantial, ambiguous, architectural, multi-stakeholder, or risky work | proven | [align-project](../../skills/align-project/SKILL.md) |
| Human-forced alignment and bounded-work skip rationale without approval/handoff | proven | [align-project](../../skills/align-project/SKILL.md), [bounded-skip case](../../evals/cases/bounded-skip.md), and captured example under [runs](../evals/runs/bounded-skip) |
| Restart after context loss resumes from files at the first incomplete phase | proven | Fresh-context file-state application in [workflow application evidence](workflow-application-evidence.md), [align-project](../../skills/align-project/SKILL.md), and resume-mapping regression in [skill tests](../../tests/test_skills.py) |
| Discovery separates facts, statements, outcomes, constraints, inferences, assumptions, contradictions, and questions | proven | [discover-domain](../../skills/discover-domain/SKILL.md) and discovery templates under [templates](../../templates/alignment) |
| Discovery asks one material question at a time | proven | [discover-domain](../../skills/discover-domain/SKILL.md) |
| Cockburn use cases include the specified goal-oriented fields | proven | [Cockburn reference](../../references/cockburn.md), [write-use-cases](../../skills/write-use-cases/SKILL.md), and [approved UC-001](../../examples/approved-project/alignment/use-cases/UC-001.md) |
| BDD covers observable priority paths/extensions with readable relationships and proposed inference labels | proven | [BDD reference](../../references/bdd.md), [specify-behavior](../../skills/specify-behavior/SKILL.md), [approved feature](../../examples/approved-project/alignment/features/release-handoff.feature), and manually inspected [independent invocation](skill-invocations/specify-behavior/transcript.md) |
| C4 context/containers/components are used at the specified depth | proven | [C4 reference](../../references/c4.md), [model-architecture](../../skills/model-architecture/SKILL.md), and approved architecture files under [examples](../../examples/approved-project/alignment/architecture) |
| Material architecture choices become ADRs | proven | [model-architecture](../../skills/model-architecture/SKILL.md) and [ADR-001](../../examples/approved-project/alignment/decisions/ADR-001.md) |
| Semantic review checks all seven specified gap classes and writes findings | proven | [semantic-review reference](../../references/semantic-review.md), [review skill](../../skills/review-alignment/SKILL.md), and [approved review](../../examples/approved-project/alignment/review.md) |
| Semantic findings remain human-review records, not compiler diagnostics | proven | [review skill](../../skills/review-alignment/SKILL.md) and [trust model](../../docs/trust-model.md) |
| Presentation shows understanding and uncertainty | proven | [build-review](../../skills/build-review/SKILL.md), [review payload](../../examples/approved-project/alignment-review/site/public/review.json), and Site suites |
| Current human reply may be simply approved/changes_requested/rejected | proven | [approve-handoff](../../skills/approve-handoff/SKILL.md) and `tests.test_release.ReleaseTests.test_agent_binds_a_simple_human_decision_to_the_issued_digest` |
| Human need not repeat a digest; agent binds current reply internally | proven | [usage](../../docs/usage.md), [approve-handoff](../../skills/approve-handoff/SKILL.md), and the same release test |
| Decision cannot bind to a superseded issuance | proven | [approve-handoff](../../skills/approve-handoff/SKILL.md) and exact-hash/stale tests in [approval suite](../../tests/test_approval_gate.py) |
| `changes_requested` returns to revision | proven | [approval reference](../../references/approval.md), [recovery guide](../../docs/recovery.md), and gate outcome test |
| `rejected` closes without handoff | proven | [approval reference](../../references/approval.md), [recovery guide](../../docs/recovery.md), and gate outcome test |
| `approved` unlocks handoff only for the unchanged reviewed snapshot | proven | [approval tests](../../tests/test_approval_gate.py), approved example gate, and [E2E evidence](e2e.json) |
| Handoff transitions to `superpowers:brainstorming` with dossier context | proven | [approved handoff](../../examples/approved-project/alignment/handoff.md) and SHA-bound [intake evidence](superpowers-intake.md) |
| Pending handoff resume rechecks freshness before any decision or delivery action | proven | Fresh-context RED/GREEN [resume transcript](skill-invocations/approve-handoff-resume.md), structured [provenance](skill-invocations/approve-handoff-resume.json), early [approve-handoff branch](../../skills/approve-handoff/SKILL.md), and mechanical regressions in [skill tests](../../tests/test_skills.py) and [release tests](../../tests/test_release.py) |
| Superpowers-unavailable delivery stays pending without approval/handoff mutation | proven | RED/GREEN fresh-context application in [workflow application evidence](workflow-application-evidence.md), conditional [approve-handoff skill](../../skills/approve-handoff/SKILL.md), and durable skill regression in [skill tests](../../tests/test_skills.py) |

## Dossier contract

| Artifact | Status | Concrete evidence |
| --- | --- | --- |
| `alignment/manifest.yaml` | proven | [template](../../templates/alignment/manifest.yaml), [approved example](../../examples/approved-project/alignment/manifest.yaml), and init tests |
| `alignment/charter.md` | proven | [template](../../templates/alignment/charter.md) and [approved example](../../examples/approved-project/alignment/charter.md) |
| `alignment/stakeholders.md` | proven | [template](../../templates/alignment/stakeholders.md) and [approved example](../../examples/approved-project/alignment/stakeholders.md) |
| `alignment/glossary.md` | proven | [template](../../templates/alignment/glossary.md) and [approved example](../../examples/approved-project/alignment/glossary.md) |
| `alignment/assumptions.md` | proven | [template](../../templates/alignment/assumptions.md) and [approved example](../../examples/approved-project/alignment/assumptions.md) |
| `alignment/open-questions.md` | proven | [template](../../templates/alignment/open-questions.md) and [approved example](../../examples/approved-project/alignment/open-questions.md) |
| `alignment/use-cases/UC-*.md` | proven | Template directory plus [UC-001](../../examples/approved-project/alignment/use-cases/UC-001.md) and clean-install artifact inventory |
| `alignment/features/*.feature` | proven | Template directory plus [release-handoff.feature](../../examples/approved-project/alignment/features/release-handoff.feature) and clean-install artifact inventory |
| `alignment/architecture/context.md` | proven | [template](../../templates/alignment/architecture/context.md) and [approved example](../../examples/approved-project/alignment/architecture/context.md) |
| `alignment/architecture/containers.md` | proven | [template](../../templates/alignment/architecture/containers.md) and [approved example](../../examples/approved-project/alignment/architecture/containers.md) |
| `alignment/architecture/components.md` | proven | [template](../../templates/alignment/architecture/components.md) and [approved example](../../examples/approved-project/alignment/architecture/components.md) |
| `alignment/decisions/ADR-*.md` | proven | Template directory plus [ADR-001](../../examples/approved-project/alignment/decisions/ADR-001.md) |
| `alignment/review.md` human-readable findings | proven | [template](../../templates/alignment/review.md) and [approved review](../../examples/approved-project/alignment/review.md) |
| `alignment/review-state.json` process state | proven | [template](../../templates/alignment/review-state.json), [approved state](../../examples/approved-project/alignment/review-state.json), and approval tests |
| `alignment/handoff.md` absent before and generated only after gate | proven | Init test asserts absence; approval suite asserts guarded creation; [approved handoff](../../examples/approved-project/alignment/handoff.md) is helper-generated |
| `alignment-review/` is derived/rebuildable presentation output | proven | [artifact contract](../../references/artifact-contract.md), [Site template](../../adapters/codex-site/template), and [approved Site](../../examples/approved-project/alignment-review/site) |
| Manifest is JSON-compatible YAML and helper checks shape/path safety only | proven | [manifest template](../../templates/alignment/manifest.yaml), [artifacts module](../../src/epistemic_alignment/artifacts.py), and thin-boundary/snapshot tests |
| Stable IDs/cross-links are human-readable conventions, not a database schema | proven | [artifact contract](../../references/artifact-contract.md), approved dossier IDs, and [trust model](../../docs/trust-model.md) |

## Thin snapshot and approval gate

| Mechanical rule | Status | Concrete evidence |
| --- | --- | --- |
| Algorithm is `sha256-v1` over manifest-declared paths | proven | [snapshot implementation](../../src/epistemic_alignment/snapshot.py), snapshot tests, and approved snapshot command |
| Missing, duplicate, non-file, unsafe, or escaping paths fail closed | proven | `test_unsafe_duplicate_missing_and_non_file_paths_fail_closed` and `test_symlinks_resolving_outside_dossier_fail_closed` in [snapshot tests](../../tests/test_snapshot.py) |
| Sorted POSIX paths, UTF-8, LF normalization, and unambiguous framing are deterministic | proven | deterministic and boundary-ambiguity tests in [snapshot tests](../../tests/test_snapshot.py) |
| Included text with invalid UTF-8 is rejected by the real snapshot path | proven | Direct production-behavior characterization `test_real_snapshot_path_rejects_invalid_utf8` in [snapshot tests](../../tests/test_snapshot.py) |
| Included-file edits change the digest | proven | `test_included_file_change_changes_hash` in [snapshot tests](../../tests/test_snapshot.py) |
| Review state/handoff/presentation/timestamps/renderer state/stored hashes are excluded | proven | [snapshot implementation](../../src/epistemic_alignment/snapshot.py), [artifact contract](../../references/artifact-contract.md), and snapshot-membership skill test |
| Helper never parses or judges document semantics | proven | [thin dossier boundary](../../src/epistemic_alignment/artifacts.py), [models](../../src/epistemic_alignment/models.py), and negative audit |
| Review state records snapshot, presentation, decision, finding acknowledgement, and handoff verification | proven | [approval implementation](../../src/epistemic_alignment/approval.py), [handoff implementation](../../src/epistemic_alignment/handoff.py), and [approved state](../../examples/approved-project/alignment/review-state.json) |
| Handoff readiness binds exact helper-generated bytes and rejects an unrecorded file, malformed/mismatched hash, symlink, non-regular file, or unresolved transaction | proven | Exact-byte tamper, unrecorded-file, hash, symlink, transaction-window, and rollback regressions in [approval tests](../../tests/test_approval_gate.py); [approved state](../../examples/approved-project/alignment/review-state.json) records `content_sha256` |
| Reviewer label is descriptive, not authenticated identity | proven | [trust model](../../docs/trust-model.md), [approved review FINDING-001](../../examples/approved-project/alignment/review.md), and acknowledged release decision |
| Current, issued, rendered, approved, and handoff hashes are equal | proven | Exact-hash tests, approved snapshot/check commands, and [E2E evidence](e2e.json) |
| Presentation status is `presented` or `published` before approval | proven | Approval tests for unpresented review and [approval implementation](../../src/epistemic_alignment/approval.py) |
| Decision must be `approved` for readiness | proven | Gate outcome tests in [approval suite](../../tests/test_approval_gate.py) |
| Provenance must be `human-message` | proven | Agent-provenance test in [approval suite](../../tests/test_approval_gate.py) and approved release state |
| Decision belongs to current issuance | proven | Exact issued/rendered/current hash test and stale-approval tests in [approval suite](../../tests/test_approval_gate.py) |
| Supported manifest/review-state versions are required | proven | Malformed/unsupported state tests in [approval suite](../../tests/test_approval_gate.py) and manifest loader tests |
| Helper does not infer whether findings are resolved | proven | [approval reference](../../references/approval.md), [trust model](../../docs/trust-model.md), and no semantic helper code in negative audit |
| Approval skill shows review findings and transcribes explicit current decision | proven | [approve-handoff skill](../../skills/approve-handoff/SKILL.md) and release approval evidence |
| Interrupted/concurrent state writes fail closed and preserve consistency | proven | Transaction, rollback, backup, and state/file binding cases in [approval suite](../../tests/test_approval_gate.py) |

## Codex review Site

| View/rule | Status | Concrete evidence |
| --- | --- | --- |
| 1. Executive summary and goals | proven | `summary` section in [review payload](../../examples/approved-project/alignment-review/site/public/review.json) and rendered Site suite |
| 2. Stakeholder map and glossary | proven | `stakeholders` section in review payload and rendered Site suite |
| 3. Cockburn use cases | proven | `useCases` section in review payload and rendered Site suite |
| 4. BDD examples | proven | `behavior` section in review payload and rendered Site suite |
| 5. C4 diagrams and responsibilities | proven | `architecture` section, [C4 component](../../examples/approved-project/alignment-review/site/components/C4Diagram.tsx), and fallback rendered test |
| 6. ADRs, assumptions, contradictions, questions, and risks | proven | `decisions`/`risks` sections in review payload and rendered Site suite |
| 7. Findings, snapshot hash, and decision readiness | proven | `findings`/`snapshot` sections, [FindingsPanel](../../examples/approved-project/alignment-review/site/components/FindingsPanel.tsx), and finding-order rendered test |
| Every summary has a dossier path/ID and a working internal evidence link | proven | Resolved-href rendered tests in both Sites, payload source regression in [Codex Site tests](../../tests/test_codex_site.py), [EvidenceReference](../../adapters/codex-site/template/components/EvidenceReference.tsx), and [EvidenceIndex](../../adapters/codex-site/template/components/EvidenceIndex.tsx) |
| Proposed/uncertain/conflicting states use visible text labels | proven | Rendered Site suite and [Site QA](../site-qa/codex-site-qa.md) |
| No approval control or persistence exists | proven | `tests.test_codex_site`, rendered Site suite, hosting config, and [Site QA](../site-qa/codex-site-qa.md) |
| Draft build/inspection does not publish; hosting requires explicit consent | proven | [build-review skill](../../skills/build-review/SKILL.md), [usage](../../docs/usage.md), and release evidence `publication_performed: false` |
| Site failure cannot mutate dossier or manufacture presentation | proven | [recovery guide](../../docs/recovery.md), [adapter contract](../../adapters/adapter-contract.md), and read-only Site implementation |

## Test categories

| Required category | Status | Concrete evidence |
| --- | --- | --- |
| Helper: initialization and overwrite refusal | proven | Four cases in [init tests](../../tests/test_init.py) |
| Helper: safe manifest path handling | proven | Unsafe/missing/duplicate/non-file/symlink cases in [snapshot tests](../../tests/test_snapshot.py) |
| Helper: deterministic hashing across order/line endings | proven | Determinism case in snapshot tests |
| Helper: digest changes after included-file edit | proven | Edit case in snapshot tests |
| Helper: decision/presentation/generated state exclusions | proven | Snapshot implementation plus membership test in [skill tests](../../tests/test_skills.py) |
| Helper: malformed, stale, non-human, and unpresented approvals rejected | proven | Adversarial cases in [approval tests](../../tests/test_approval_gate.py) |
| Helper: successful equal-hash handoff | proven | Approved-flow case in approval tests and clean-installed release flow |
| Scenario: greenfield | proven | [case](../../evals/cases/greenfield.md) and [captured run](../evals/runs/greenfield) |
| Scenario: existing repository | proven | [case](../../evals/cases/existing-repo.md) and [captured run](../evals/runs/existing-repo) |
| Scenario: conflicting stakeholders | proven | [case](../../evals/cases/conflict.md) and [captured run](../evals/runs/conflict) |
| Scenario: critical unknown | proven | [case](../../evals/cases/critical-unknown.md) and [captured run](../evals/runs/critical-unknown) |
| Scenario: bounded skip | proven | [case](../../evals/cases/bounded-skip.md) and [captured run](../evals/runs/bounded-skip) |
| Scenario: post-approval edit | proven | [case-only walkthrough](../../evals/cases/stale-approval.md) and deterministic stale-approval helper test |
| Scenario: attempted self-approval | proven | [case-only walkthrough](../../evals/cases/self-approval.md) and deterministic agent-provenance helper test |
| Scenario corpus is non-authoritative and has no checker | proven | [eval README](../../evals/README.md); five run directories/seven cases; `scripts/check-evals` absent |
| Site: production builds and all dossier sections render | proven | Both Site `pnpm ... test` commands; 4/4 each |
| Site: desktop and narrow visual inspection | proven | [Site QA](../site-qa/codex-site-qa.md), [desktop](site-desktop.png), [narrow](site-narrow.png), and PNG metadata test |
| Site: keyboard, headings, contrast, and labelled statuses | proven | [Site QA](../site-qa/codex-site-qa.md) |
| Site: uncertainty, contradictions, findings, and digest visible | proven | Review payload, rendered Site suites, screenshots, and Site QA |
| E2E: complex request through unchanged approval to Superpowers intake | proven | [E2E evidence](e2e.json), installed-cache release test, approved example, and [SHA-bound intake](superpowers-intake.md) |

## Release criteria

| Criterion | Status | Concrete evidence |
| --- | --- | --- |
| Clean install and eight discoverable skills | proven | `tests.test_release.ReleaseTests.test_clean_install_uses_packaged_plugin_in_isolated_codex_home` |
| Python 3.9 helper with no third-party runtime dependency | proven | Full suite runs with system Python 3.9; [source](../../src/epistemic_alignment) imports standard library only; PyYAML is isolated to validator recipe |
| No semantic parser/validator | proven | Prescribed negative `rg` audit and thin-boundary tests |
| Helper tests prove mechanical snapshot/approval integrity | proven | Full Python suite, especially snapshot and approval suites |
| Illustrative examples document method/prohibited behavior for manual inspection | proven | [eval README](../../evals/README.md), seven cases, five captures, and two walkthroughs |
| Example Site builds and passes visual/accessibility inspection | proven | Approved-example Site suite, [Site QA](../site-qa/codex-site-qa.md), and verified screenshots |
| Clean-installed E2E reaches Superpowers only after unchanged human approval | proven | Installed-cache release test, exact release state, [E2E evidence](e2e.json), and [intake evidence](superpowers-intake.md) |
| Installation, usage, recovery, trust boundary, and removal documented | proven | [installation](../../docs/installation.md), [usage](../../docs/usage.md), [recovery](../../docs/recovery.md), and [trust model](../../docs/trust-model.md) |
| Adapter contract and concrete Claude/OpenCode/Qwen Code road maps included | proven | [contract](../../adapters/adapter-contract.md), [Claude](../../adapters/claude.md), [OpenCode](../../adapters/opencode.md), and [Qwen Code](../../adapters/qwen-code.md) |

## Future-adapter deliverables

| Deliverable | Status | Concrete evidence |
| --- | --- | --- |
| Common renderer input/output, capability, fallback, hash, and host-boundary contract | proven | [adapter contract](../../adapters/adapter-contract.md) |
| Claude Artifact road map preserving the seven views and display-only approval boundary | proven | [Claude road map](../../adapters/claude.md) |
| OpenCode local-static road map with separate extension metadata and preview command | proven | [OpenCode road map](../../adapters/opencode.md) |
| Qwen Code shared-renderer road map with separate metadata and preview command | proven | [Qwen Code road map](../../adapters/qwen-code.md) |

## GitHub-ready release metadata

| Deliverable | Status | Concrete evidence |
| --- | --- | --- |
| Manifest version, keywords, capabilities, and PNG screenshots | proven | [manifest](../../.codex-plugin/plugin.json), [assets](../../assets), metadata test, and pinned plugin validation |
| No invented repository/homepage fields before a remote exists | proven | `git remote -v` is empty; manifest metadata test asserts the omissions |
| Generated Python/Node/Sites output ignored | proven | [.gitignore](../../.gitignore), `git status --short --ignored`, and no generated paths in `git ls-files` |
| v0.1.0 release history | proven | [CHANGELOG](../../CHANGELOG.md) |
| Exact local verification recipe | proven | [README verification](../../README.md) covers Task 8, focused release, both Site, snapshot/gate, and pinned PyYAML validator commands |
| Recommended repository name and tag without publication | proven | [README release metadata](../../README.md) recommends `epistemic-alignment` and `v0.1.0`; no remote, push, tag, marketplace install, or publication is performed by Task 8 |

## Final command evidence

The release decision is based on current commands, not the illustrative eval
corpus:

```sh
git diff --check
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m unittest tests.test_release -v
pnpm --dir adapters/codex-site/template test
pnpm --dir examples/approved-project/alignment-review/site test
scripts/alignment snapshot examples/approved-project --json
scripts/alignment check examples/approved-project --json
! rg -n "class Entity|ValidationReport|the semantic validator passed|coverage.*complete" src tests
git status --short
```

Plugin validation uses a fresh venv with pinned `PyYAML==6.0.2` and
plugin-creator's `validate_plugin.py`, as documented in the [README](../../README.md).
There is deliberately no eval-checker command, publication, remote creation,
push, tag creation, or personal-marketplace mutation in this audit.
