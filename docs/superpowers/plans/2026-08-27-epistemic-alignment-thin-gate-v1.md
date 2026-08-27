# Epistemic Alignment Thin-Gate Codex v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish a Codex-first alignment plugin whose skills produce discovery, Cockburn, BDD, C4, semantic review, and a ChatGPT Site, while a minimal helper protects only snapshot and human-approval integrity before Superpowers handoff.

**Architecture:** Tasks 1–2 of the superseded plan already produced the plugin skeleton and initializer. This continuation removes their premature entity parser, adds a dependency-free snapshot/approval helper, then builds the method skills and Codex Site. Semantic quality remains the responsibility of skills and humans; deterministic code never claims to validate requirements, coverage, architecture, or consensus.

**Tech Stack:** Codex plugin manifest; Markdown skills; Python 3.9 standard library; `unittest`; JSON-compatible YAML; Gherkin; Mermaid; React 19.2.6; TypeScript 5.9.3; vinext 1.0.0-beta.2; Mermaid 11.17.2; ChatGPT Sites.

**Spec:** `docs/superpowers/specs/2026-08-27-epistemic-alignment-plugin-design.md`

## Starting state

- `4013934` implemented and reviewed the plugin/CLI skeleton.
- `5eb2e3e` implemented dossier initialization.
- `405a91e` fixed JSON-special project metadata and passed scoped re-review.
- `480eb4d` revised the design to the approved thin-gate architecture.
- The old validator Task 3 was interrupted before commit; its untracked test was removed.

## Global Constraints

- The package is skills plus a thin deterministic helper, not a semantic parser, requirements compiler, or agent runtime.
- Python runtime floor is 3.9; helper runtime dependencies are standard library only.
- Canonical source lives under target `alignment/`; generated review output lives under `alignment-review/`.
- Model judgment and human review own use-case quality, BDD completeness, C4 correctness, traceability, contradictions, and readiness.
- The helper may initialize files, verify manifest/path safety, hash snapshots, record explicit decisions, detect stale approval, and create handoff only.
- No `Entity` model, document-front-matter parser, ID graph, semantic diagnostic, or machine coverage calculation may remain.
- Approval requires an explicit current-interaction human message; the helper verifies `human-message` provenance but does not claim authenticated identity.
- Issued, rendered, approved, and current `sha256-v1` hashes must match before handoff.
- Publishing or updating a Site requires explicit human consent; draft build and local/ChatGPT inspection do not.
- Codex v1 ships production skills and Site behavior; Claude, OpenCode, and Qwen Code receive a concrete adapter contract and road maps.
- Each task follows TDD, produces focused evidence, commits, and receives independent task review.

## File map

```text
src/epistemic_alignment/
  models.py       Dossier, Snapshot, GateResult data only
  artifacts.py    Initialization and manifest/path loading only
  snapshot.py     Safe path resolution and sha256-v1
  approval.py     Review issuance, decision transcription, freshness gate
  handoff.py      Thin approved-snapshot handoff document
  cli.py          init/snapshot/issue-review/decide/check/handoff commands
templates/alignment/                 Human-readable dossier templates
skills/{align-project,...}/          Eight portable method skills
skills/shared/references/            Cockburn, BDD, C4, review, gate, adapters
adapters/codex-site/template/        Presentational Sites application
adapters/*.md                         Cross-harness contract and road maps
evals/                                Scenario cases and evidence
examples/approved-project/            Verified end-to-end example
```

---

### Task 1: Remove semantic parsing and establish the thin dossier boundary

**Files:**
- Modify: `src/epistemic_alignment/models.py`
- Modify: `src/epistemic_alignment/artifacts.py`
- Modify: `templates/alignment/manifest.yaml`
- Create: `templates/alignment/review.md`
- Modify: `templates/alignment/review-state.json`
- Modify: `tests/test_init.py`
- Create: `tests/test_thin_boundary.py`

**Interfaces:**
- Consumes: reviewed initializer from commit `405a91e`.
- Produces: `Dossier(root: Path, manifest: dict, snapshot_paths: list[str])`; `load_dossier(alignment_dir: Path) -> Dossier`; no document-semantic types or parsing.

- [ ] **Step 1: Write failing thin-boundary tests**

```python
# tests/test_thin_boundary.py
import unittest
from pathlib import Path
from epistemic_alignment import models
from epistemic_alignment.artifacts import load_dossier

FIXTURE = Path(__file__).parents[1] / "templates/alignment"


class ThinBoundaryTests(unittest.TestCase):
    def test_dossier_loads_manifest_without_parsing_documents(self):
        dossier = load_dossier(FIXTURE)
        self.assertEqual(dossier.manifest["schema_version"], "1.0")
        self.assertIn("charter.md", dossier.snapshot_paths)
        self.assertIn("review.md", dossier.snapshot_paths)

    def test_semantic_entity_model_is_absent(self):
        self.assertFalse(hasattr(models, "Entity"))
        self.assertFalse(hasattr(models, "ValidationReport"))
```

Update `tests/test_init.py` to call `load_dossier` and assert the initialized manifest uses `snapshot_paths`, contains `review.md`, and creates no `handoff.md`.

- [ ] **Step 2: Run tests and confirm the old parser violates the boundary**

Run: `PYTHONPATH=src python3 -m unittest tests.test_thin_boundary tests.test_init -v`

Expected: import failure for `load_dossier` and failure because `Entity` still exists.

- [ ] **Step 3: Implement the minimal dossier model**

```python
# src/epistemic_alignment/models.py
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class Dossier:
    root: Path
    manifest: Dict[str, Any]
    snapshot_paths: List[str]
```

`load_dossier` parses only `manifest.yaml`, verifies `schema_version == "1.0"`, verifies `snapshot_paths` is a list of strings, and returns `Dossier`. Remove `_front_matter`, `Entity`, `ArtifactSet`, and entity collection.

The initial manifest retains project/phase/renderer fields and declares these snapshot paths:

```json
[
  "charter.md",
  "stakeholders.md",
  "glossary.md",
  "assumptions.md",
  "open-questions.md",
  "architecture/context.md",
  "architecture/containers.md",
  "architecture/components.md",
  "review.md"
]
```

`review-state.json` contains `schema_version`, empty `snapshot`, `presentation`, `decision`, and `handoff` objects. It is process state and is not a snapshot path.

- [ ] **Step 4: Run focused and full tests**

Run: `PYTHONPATH=src python3 -m unittest tests.test_thin_boundary tests.test_init -v`

Expected: all focused tests pass.

Run: `PYTHONPATH=src python3 -m unittest discover -s tests -v`

Expected: full suite passes with no semantic parser modules or tests.

- [ ] **Step 5: Commit the boundary correction**

```bash
git add src/epistemic_alignment templates/alignment tests
git commit -m "refactor: reduce artifacts to a thin dossier boundary"
```

---

### Task 2: Safe snapshot hashing

**Files:**
- Modify: `src/epistemic_alignment/models.py`
- Modify: `src/epistemic_alignment/artifacts.py`
- Create: `src/epistemic_alignment/snapshot.py`
- Modify: `src/epistemic_alignment/cli.py`
- Create: `tests/test_snapshot.py`

**Interfaces:**
- Consumes: `Dossier.snapshot_paths`.
- Produces: `Snapshot(algorithm: str, digest: str, paths: list[str])`; `create_snapshot(alignment_dir: Path) -> Snapshot`; CLI `alignment snapshot ROOT [--json]`.

- [ ] **Step 1: Write failing deterministic and unsafe-path tests**

```python
# tests/test_snapshot.py
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from epistemic_alignment.snapshot import create_snapshot

TEMPLATE = Path(__file__).parents[1] / "templates/alignment"


class SnapshotTests(unittest.TestCase):
    def copy_dossier(self, directory):
        target = Path(directory) / "alignment"
        shutil.copytree(TEMPLATE, target)
        return target

    def test_hash_is_stable_across_manifest_path_order_and_crlf(self):
        with tempfile.TemporaryDirectory() as directory:
            left = self.copy_dossier(Path(directory) / "left")
            right = self.copy_dossier(Path(directory) / "right")
            manifest = json.loads((right / "manifest.yaml").read_text())
            manifest["snapshot_paths"].reverse()
            (right / "manifest.yaml").write_text(json.dumps(manifest))
            charter = (right / "charter.md").read_text()
            (right / "charter.md").write_bytes(charter.replace("\n", "\r\n").encode())
            self.assertEqual(create_snapshot(left).digest, create_snapshot(right).digest)

    def test_included_file_change_changes_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.copy_dossier(directory)
            before = create_snapshot(target).digest
            (target / "charter.md").write_text((target / "charter.md").read_text() + "\nChanged\n")
            self.assertNotEqual(before, create_snapshot(target).digest)

    def test_escape_duplicate_and_missing_paths_fail_closed(self):
        for bad_paths in [["../secret"], ["charter.md", "charter.md"], ["missing.md"]]:
            with self.subTest(paths=bad_paths), tempfile.TemporaryDirectory() as directory:
                target = self.copy_dossier(directory)
                manifest = json.loads((target / "manifest.yaml").read_text())
                manifest["snapshot_paths"] = bad_paths
                (target / "manifest.yaml").write_text(json.dumps(manifest))
                with self.assertRaises(ValueError):
                    create_snapshot(target)
```

- [ ] **Step 2: Run tests and verify the snapshot module is absent**

Run: `PYTHONPATH=src python3 -m unittest tests.test_snapshot -v`

Expected: import failure for `epistemic_alignment.snapshot`.

- [ ] **Step 3: Implement `sha256-v1` without semantic parsing**

```python
# addition to models.py
@dataclass(frozen=True)
class Snapshot:
    algorithm: str
    digest: str
    paths: List[str]
```

For each unique manifest path: require a relative POSIX path with no empty, `.` or `..` segment; resolve it under `alignment/`; reject escape, missing/non-file targets, and symlinks resolving outside the dossier. Hash a canonical header containing only schema version, project identity, and sorted snapshot paths, followed by each path, NUL, normalized UTF-8 content, NUL. Normalize CRLF/CR to LF. Sort paths. Label the result `sha256-v1`.

- [ ] **Step 4: Add CLI and run tests**

Run: `PYTHONPATH=src python3 -m unittest tests.test_snapshot -v`

Expected: all snapshot tests pass.

Run: `scripts/alignment snapshot templates --json`

Expected: JSON with `algorithm: sha256-v1`, a 64-character digest, and sorted paths.

Run: `PYTHONPATH=src python3 -m unittest discover -s tests -v`

Expected: full suite passes.

- [ ] **Step 5: Commit snapshot integrity**

```bash
git add src tests/test_snapshot.py
git commit -m "feat: hash reviewed dossier snapshots"
```

---

### Task 3: Human decision and stale-approval gate

**Files:**
- Modify: `src/epistemic_alignment/models.py`
- Create: `src/epistemic_alignment/approval.py`
- Create: `src/epistemic_alignment/handoff.py`
- Modify: `src/epistemic_alignment/cli.py`
- Create: `tests/test_approval_gate.py`

**Interfaces:**
- Consumes: `create_snapshot`, `review-state.json`, project identity and snapshot paths.
- Produces: `issue_review(alignment_dir: Path, adapter: str, status: str, location: str) -> Snapshot`; `record_decision(alignment_dir: Path, decision: str, reviewer: str, provenance: str, review_hash: str, acknowledged_findings: list[str]) -> None`; `check_gate(alignment_dir: Path) -> GateResult`; `write_handoff(alignment_dir: Path) -> Path`; CLI `issue-review`, `decide`, `check`, `handoff`.

- [ ] **Step 1: Write failing gate tests**

```python
# tests/test_approval_gate.py
import shutil
import tempfile
import unittest
from pathlib import Path
from epistemic_alignment.approval import issue_review, record_decision, check_gate
from epistemic_alignment.handoff import write_handoff

TEMPLATE = Path(__file__).parents[1] / "templates/alignment"


class ApprovalGateTests(unittest.TestCase):
    def dossier(self, directory):
        target = Path(directory) / "alignment"
        shutil.copytree(TEMPLATE, target)
        return target

    def test_unchanged_human_approved_presented_snapshot_can_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            issued = issue_review(target, "codex-sites", "presented", "site://review")
            record_decision(target, "approved", "owner", "human-message", issued.digest, [])
            self.assertTrue(check_gate(target).ready)
            handoff = write_handoff(target)
            self.assertIn(issued.digest, handoff.read_text())
            self.assertIn("superpowers:brainstorming", handoff.read_text())

    def test_agent_provenance_and_unpresented_review_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            issued = issue_review(target, "codex-sites", "draft", "site://draft")
            with self.assertRaises(ValueError):
                record_decision(target, "approved", "agent", "agent-inference", issued.digest, [])

    def test_post_approval_edit_blocks_and_removes_handoff_readiness(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            issued = issue_review(target, "codex-sites", "presented", "site://review")
            record_decision(target, "approved", "owner", "human-message", issued.digest, [])
            (target / "review.md").write_text("changed")
            gate = check_gate(target)
            self.assertFalse(gate.ready)
            self.assertIn("stale-approval", gate.reasons)
```

- [ ] **Step 2: Run tests and confirm gate modules are absent**

Run: `PYTHONPATH=src python3 -m unittest tests.test_approval_gate -v`

Expected: imports fail for `approval` and `handoff`.

- [ ] **Step 3: Implement exact review-state transitions**

`issue_review` computes the current snapshot, requires presentation status `draft`, `presented`, or `published`, stores issued/rendered hash, adapter/location, UTC timestamp, and clears decision/handoff. `record_decision` accepts `approved`, `changes_requested`, or `rejected`; `approved` requires `human-message`, `presented|published`, and an argument hash equal to issued/rendered/current hashes. `check_gate` recomputes every time and returns `GateResult(ready: bool, reasons: list[str], digest: str)`.

```python
# addition to models.py
@dataclass(frozen=True)
class GateResult:
    ready: bool
    reasons: List[str]
    digest: str
```

`write_handoff` refuses unless `check_gate.ready`. It writes project title, `sha256-v1:<digest>`, snapshot path list, `review.md` reference, acknowledged findings, and the instruction to invoke `superpowers:brainstorming` with the dossier as required context. It updates only the handoff section of process state.

- [ ] **Step 4: Run gate and full tests**

Run: `PYTHONPATH=src python3 -m unittest tests.test_approval_gate -v`

Expected: all gate tests pass.

Run: `PYTHONPATH=src python3 -m unittest discover -s tests -v`

Expected: full suite passes.

- [ ] **Step 5: Commit the approval gate**

```bash
git add src tests/test_approval_gate.py
git commit -m "feat: gate handoff on an unchanged human-approved snapshot"
```

---

### Task 4: Portable alignment skill suite

**Files:**
- Create: `skills/align-project/SKILL.md`
- Create: `skills/discover-domain/SKILL.md`
- Create: `skills/write-use-cases/SKILL.md`
- Create: `skills/specify-behavior/SKILL.md`
- Create: `skills/model-architecture/SKILL.md`
- Create: `skills/review-alignment/SKILL.md`
- Create: `skills/build-review/SKILL.md`
- Create: `skills/approve-handoff/SKILL.md`
- Create: `skills/shared/references/{artifact-contract,cockburn,bdd,c4,semantic-review,approval,platform-detection}.md`
- Create: `tests/test_skills.py`

**Interfaces:**
- Consumes: initializer, snapshot, decision, check, and handoff CLI commands.
- Produces: eight `alignment:*` skills; semantic review in `alignment/review.md`; no semantic helper calls.

- [ ] **Step 1: Invoke `superpowers:writing-skills` and write failing structure/boundary tests**

```python
# tests/test_skills.py
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
EXPECTED = {
    "align-project", "discover-domain", "write-use-cases", "specify-behavior",
    "model-architecture", "review-alignment", "build-review", "approve-handoff",
}


class SkillTests(unittest.TestCase):
    def test_exact_skill_set(self):
        found = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(found, EXPECTED)

    def test_semantic_review_never_claims_machine_proof(self):
        text = (ROOT / "skills/review-alignment/SKILL.md").read_text()
        self.assertIn("human judgment", text)
        self.assertIn("review.md", text)
        for forbidden in ["the semantic validator passed", "coverage is complete", "architecture is correct"]:
            self.assertNotIn(forbidden, text.lower())

    def test_handoff_skill_has_explicit_human_and_hash_gate(self):
        text = (ROOT / "skills/approve-handoff/SKILL.md").read_text()
        for phrase in ["explicit human message", "human-message", "current snapshot", "never self-approve", "superpowers:brainstorming"]:
            self.assertIn(phrase, text)
```

- [ ] **Step 2: Run tests and confirm skills are absent**

Run: `python3 -m unittest tests.test_skills -v`

Expected: failures for missing skill directories.

- [ ] **Step 3: Author method references and skills**

Every skill has trigger-focused front matter, exact inputs/outputs, one-question-at-a-time interaction where appropriate, restart behavior based on files, forbidden behaviors, and one next transition. Cockburn/BDD/C4 references contain the agreed human-readable templates. Semantic review explicitly looks for unsupported goals, missing examples, unexplained responsibilities, consequences, contradictions, hidden assumptions, and critical unknowns, then writes findings rather than a pass certificate.

`approve-handoff` shows the Site reference, `review.md`, findings, and snapshot hash to the human; only after a current explicit decision does it call `decide` and `handoff`. Silence, generic prior permission, a Site button, agent confidence, or a pre-edited state file never count as approval.

- [ ] **Step 4: Run skill tests and reference audit**

Run: `python3 -m unittest tests.test_skills -v`

Run: `rg -n "validator|coverage.*complete|self-approve|scripts/alignment|superpowers:" skills`

Expected: no semantic-validator dependency; only the approval skill transitions to Superpowers; all referenced files exist.

- [ ] **Step 5: Commit skills**

```bash
git add skills tests/test_skills.py
git commit -m "feat: add thin-gate alignment skill suite"
```

---

### Task 5: Codex ChatGPT Sites review

**Files:**
- Modify: `.gitignore`
- Create: `adapters/codex-site/template/.openai/hosting.json`
- Create: `adapters/codex-site/template/{package.json,pnpm-lock.yaml,tsconfig.json,next-env.d.ts}`
- Create: `adapters/codex-site/template/{vite.config.ts,next.config.ts,postcss.config.mjs,eslint.config.mjs}`
- Create: `adapters/codex-site/template/worker/index.ts`
- Create: `adapters/codex-site/template/app/{layout.tsx,page.tsx,globals.css}`
- Create: `adapters/codex-site/template/components/{Shell,StatusBadge,SectionNav,C4Diagram,FindingsPanel}.tsx`
- Create: `adapters/codex-site/template/public/review.json`
- Create: `adapters/codex-site/template/tests/rendered-html.test.mjs`
- Create: `tests/test_codex_site.py`
- Modify: `skills/build-review/SKILL.md`

**Interfaces:**
- Consumes: dossier files, `review.md`, and current `sha256-v1` snapshot.
- Produces: presentational Sites project at `alignment-review/site`; rendered hash exactly equal to issued snapshot; no approval mutation.

- [ ] **Step 1: Invoke `sites:sites-building` and write failing adapter tests**

```python
# tests/test_codex_site.py
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SITE = ROOT / "adapters/codex-site/template"


class CodexSiteTests(unittest.TestCase):
    def test_hosting_has_no_persistence_bindings(self):
        self.assertEqual(json.loads((SITE / ".openai/hosting.json").read_text()), {"d1": None, "r2": None})

    def test_review_payload_is_presentational(self):
        data = json.loads((SITE / "public/review.json").read_text())
        self.assertIn("snapshot", data)
        self.assertIn("findings", data)
        self.assertNotIn("approveAction", data)
        self.assertNotIn("decisionMutation", data)
```

- [ ] **Step 2: Run tests and confirm Site files are absent**

Run: `python3 -m unittest tests.test_codex_site -v`

Expected: missing-file failures.

- [ ] **Step 3: Build the presentational Site template and skill workflow**

Use the current Sites vinext starter, remove persistence/auth/database code, pin React 19.2.6, React DOM 19.2.6, TypeScript 5.9.3, vinext 1.0.0-beta.2, and Mermaid 11.17.2. Add generated-output ignores before dependency installation.

The seven anchored sections are summary, stakeholders, use-cases, behavior, architecture, decisions-and-risks, and review-readiness. Proposed/uncertain/conflicting states require text labels, not color alone. Findings remain above the snapshot readiness panel. C4 Mermaid source has an accessible textual fallback. No UI control writes approval.

`public/review.json` has exact top-level keys `project`, `summary`, `stakeholders`, `useCases`, `behavior`, `architecture`, `decisions`, `risks`, `findings`, and `snapshot`. It is presentation input authored from the dossier by the skill, not a semantic certificate or canonical source.

`build-review` instructs Codex to use Sites, read the dossier semantically, populate a review payload and pages, build and inspect the draft, then call `issue-review` with the exact rendered hash. Hosting occurs only after explicit consent.

- [ ] **Step 4: Build, test, lint, and visually inspect**

Set the bundled toolchain for this workspace:

```bash
export PATH=/Users/darasokolovskaa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin:/Users/darasokolovskaa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback:$PATH
```

Run: `pnpm --dir adapters/codex-site/template install --frozen-lockfile`

Run: `pnpm --dir adapters/codex-site/template test`

Run: `pnpm --dir adapters/codex-site/template lint`

Expected: build/test/lint pass. Inspect desktop and narrow viewport with the browser, keyboard navigation, heading hierarchy, contrast, status labels, findings visibility, C4 fallback, and displayed hash.

- [ ] **Step 5: Commit Site adapter and QA evidence**

```bash
git add .gitignore adapters/codex-site skills/build-review tests/test_codex_site.py artifacts/site-qa
git commit -m "feat: present alignment dossiers with ChatGPT Sites"
```

---

### Task 6: Scenario evals and cross-harness adapter contract

**Files:**
- Create: `adapters/adapter-contract.md`
- Create: `adapters/{claude,opencode,qwen-code}.md`
- Create: `evals/README.md`
- Create: `evals/cases/{greenfield,existing-repo,conflict,critical-unknown,bounded-skip,stale-approval,self-approval}.md`
- Create: `evals/expected/*.json`
- Create: `scripts/check-evals`
- Create: `tests/test_evals.py`
- Create: `artifacts/evals/results.json`

**Interfaces:**
- Consumes: installed skills, helper commands, and Sites adapter.
- Produces: seven reproducible behavioral cases; adapter input/output contract; concrete host road maps.

- [ ] **Step 1: Write failing corpus tests**

```python
# tests/test_evals.py
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
NAMES = {"greenfield", "existing-repo", "conflict", "critical-unknown", "bounded-skip", "stale-approval", "self-approval"}


class EvalTests(unittest.TestCase):
    def test_cases_and_assertions_are_complete(self):
        self.assertEqual({p.stem for p in (ROOT / "evals/cases").glob("*.md")}, NAMES)
        self.assertEqual({p.stem for p in (ROOT / "evals/expected").glob("*.json")}, NAMES)
        for name in NAMES:
            expected = json.loads((ROOT / f"evals/expected/{name}.json").read_text())
            self.assertTrue(expected["required"])
            self.assertTrue(expected["forbidden"])
            self.assertIn(expected["gate"], {"approved", "blocked", "skipped", "invalidated"})
```

- [ ] **Step 2: Run tests and confirm corpus is absent**

Run: `python3 -m unittest tests.test_evals -v`

Expected: assertion failure for empty case sets.

- [ ] **Step 3: Author evals, checker, and adapter docs**

Each case includes starting prompt, available evidence, scripted human answers, expected dossier/Site behavior, forbidden claims, and gate result. The checker compares captured results with assertions. Conflict and critical-unknown cases must preserve findings rather than claim machine invalidity; stale/self-approval cases must fail through the thin gate. Make `scripts/check-evals` executable before its first run.

The adapter contract takes dossier path, snapshot paths/hash, semantic review, and host capabilities and returns adapter/version/location/status/rendered hash/warnings. Claude uses an Artifact; OpenCode and Qwen Code use a shared local static renderer with separate extension metadata and preview instructions.

- [ ] **Step 4: Execute and record eval evidence**

Install the development plugin and run each case in an isolated fixture. Capture dossier files, Site reference where applicable, transcript excerpts needed to prove human interaction, and gate result.

Run: `scripts/check-evals artifacts/evals/results.json`

Expected: seven cases pass and no forbidden semantic-certification or self-approval behavior occurs.

- [ ] **Step 5: Commit evals and adapter contract**

```bash
git add adapters evals scripts/check-evals tests/test_evals.py artifacts/evals
git commit -m "test: verify thin-gate alignment behavior"
```

---

### Task 7: Clean-install E2E and release documentation

**Files:**
- Modify: `README.md`
- Create: `docs/{installation,usage,recovery,trust-model,adapters}.md`
- Create: `examples/approved-project/alignment/**`
- Create: `examples/approved-project/alignment-review/site/**`
- Create: `tests/test_release.py`
- Create: `artifacts/release/e2e.json`
- Create: `artifacts/release/{site-desktop,site-narrow}.png`

**Interfaces:**
- Consumes: complete plugin, Superpowers installation, helper, skills, Site.
- Produces: verified v0.1.0 example and clean-install evidence from request to consumed handoff.

- [ ] **Step 1: Write failing release evidence tests**

```python
# tests/test_release.py
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class ReleaseTests(unittest.TestCase):
    def test_required_docs_exist(self):
        for name in ["installation", "usage", "recovery", "trust-model", "adapters"]:
            self.assertTrue((ROOT / f"docs/{name}.md").is_file(), name)

    def test_e2e_proves_unchanged_human_approved_handoff(self):
        evidence = json.loads((ROOT / "artifacts/release/e2e.json").read_text())
        self.assertEqual(evidence["plugin_version"], "0.1.0")
        self.assertTrue(evidence["site_presented"])
        self.assertTrue(evidence["human_approved"])
        self.assertEqual(evidence["issued_hash"], evidence["rendered_hash"])
        self.assertEqual(evidence["issued_hash"], evidence["approved_hash"])
        self.assertEqual(evidence["issued_hash"], evidence["handoff_hash"])
        self.assertTrue(evidence["superpowers_handoff_consumed"])
        self.assertFalse(evidence["semantic_validator_present"])
```

- [ ] **Step 2: Run tests and confirm release evidence is absent**

Run: `python3 -m unittest tests.test_release -v`

Expected: missing docs/evidence failures.

- [ ] **Step 3: Complete docs and an approved example**

Document personal plugin installation/reinstall, invocation, phase outputs, helper commands/exit codes, recovery, trust boundary, Site consent/publishing, Superpowers dependency, removal, and all adapter road maps. The example must be produced through the skills, contain `review.md`, show the Site, carry an explicit human-message approval, and generate handoff through the helper without manual hash edits.

- [ ] **Step 4: Execute clean-install E2E and full verification**

Use `plugin-creator`'s Codex development installation flow. In a clean fixture run discovery, Cockburn, BDD, C4, semantic review, Site build/inspection, explicit approval, unchanged-snapshot check, handoff generation, and Superpowers consumption. Publication remains optional and consent-gated.

Run: `PYTHONPATH=src python3 -m unittest discover -s tests -v`

Run: `scripts/alignment snapshot examples/approved-project --json`

Run: `scripts/alignment check examples/approved-project --json`

Run: `pnpm --dir examples/approved-project/alignment-review/site test`

Expected: all tests pass, gate is ready, Site builds, and E2E evidence hashes match.

- [ ] **Step 5: Commit release docs and evidence**

```bash
git add README.md docs examples tests/test_release.py artifacts/release
git commit -m "docs: prepare thin-gate Codex release"
```

---

### Task 8: Completion audit and GitHub-ready state

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `.gitignore`
- Modify: `README.md`
- Create: `CHANGELOG.md`
- Create: `artifacts/release/completion-audit.md`

**Interfaces:**
- Consumes: revised spec and all implementation/eval/release evidence.
- Produces: clean v0.1.0 repository and requirement-by-requirement proof without pushing or inventing a remote.

- [ ] **Step 1: Write the completion matrix**

Create one row for every v1 scope item, workflow phase, dossier artifact, thin-gate rule, Site view, test category, release criterion, and future-adapter deliverable. Link each to authoritative files/commands and mark `proven`, `contradicted`, or `missing`. Any non-`proven` row prevents completion.

- [ ] **Step 2: Run the full audit commands**

```bash
git diff --check
PYTHONPATH=src python3 -m unittest discover -s tests -v
scripts/check-evals artifacts/evals/results.json
pnpm --dir adapters/codex-site/template test
! rg -n "class Entity|ValidationReport|the semantic validator passed|coverage.*complete" src tests
git status --short
```

Expected: no whitespace errors; all suites pass; no semantic parser/validator implementation is found; only intended audit/release metadata remains.

- [ ] **Step 3: Resolve every non-proven audit row**

Implement and verify the original revised-spec requirement. Do not weaken requirements to match existing behavior. Record concrete evidence and rerun the affected suite.

- [ ] **Step 4: Add GitHub-ready metadata**

Finalize plugin keywords/capabilities/screenshots, generated-output ignores, changelog, and local verification commands. Recommend repository name `epistemic-alignment` and tag `v0.1.0`; add repository/homepage fields only after an actual remote exists.

- [ ] **Step 5: Commit and reverify HEAD**

```bash
git add .codex-plugin/plugin.json .gitignore README.md CHANGELOG.md artifacts/release/completion-audit.md
git commit -m "chore: finalize epistemic alignment v0.1.0"
```

Rerun every Step 2 command against `HEAD`, then compare the completion audit to the revised design spec before marking the active goal complete.
