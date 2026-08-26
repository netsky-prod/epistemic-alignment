# Epistemic Alignment Codex v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, install, and verify a Codex-first plugin package that creates traceable discovery, Cockburn use cases, BDD, C4, a ChatGPT Sites review, a human-only approval record, and a hash-verified handoff to Superpowers.

**Architecture:** The repository contains a Superpowers-style Codex plugin made of eight focused skills, portable canonical templates, and a deterministic Python 3.9 helper. The helper owns parsing, validation, hashing, readiness, approval-state checks, handoff generation, and review-data projection; the model owns semantic authoring. The Codex adapter renders the projection with the current Sites vinext stack, while a documented adapter contract preserves portability to Claude, OpenCode, and Qwen Code.

**Tech Stack:** Codex plugin manifest; Markdown skills; Python 3.9 standard library; `unittest`; JSON-compatible YAML; Gherkin; Mermaid C4 source; React 19.2.6; TypeScript 5.9.3; vinext 1.0.0-beta.2; Mermaid 11.17.2; Sites hosting configuration.

**Spec:** `docs/superpowers/specs/2026-08-27-epistemic-alignment-plugin-design.md`

## Global Constraints

- Version one is Codex-first; Claude, OpenCode, and Qwen Code receive an executable adapter contract and installation road map, not production adapters.
- The package is skills plus deterministic helpers, not a new agent runtime.
- Canonical source lives under a target project's `alignment/`; generated review output lives under `alignment-review/`.
- `manifest.yaml` and Markdown front matter use JSON syntax, which is a valid YAML 1.2 subset and can be parsed with Python's standard-library `json` module.
- Python runtime floor is 3.9; the helper has no third-party runtime dependencies.
- The site runtime floor is Node 22.13.0 and uses exact package versions recorded above and in its lockfile.
- Human approval is a workflow invariant, not cryptographic authentication; only an explicit current-interaction human message may be transcribed as `approved`.
- The helper fails closed on invalid schema, critical blockers, stale hashes, non-human provenance, unsupported schema versions, or unpresented review output.
- Semantic content changes invalidate approval; `review-state.json`, `handoff.md`, generated output, timestamps, and declared process-only manifest fields are outside the reviewed-content hash.
- Publishing a Site requires explicit human consent; draft generation and local visual verification do not.
- Every implementation task follows red-green-refactor and ends with a focused commit.

## Planned file map

```text
.codex-plugin/plugin.json               Codex plugin metadata and skill entry
README.md                               Installation, workflow, commands, trust model
LICENSE                                 MIT license
pyproject.toml                          Python metadata and runtime floor
scripts/alignment                       Portable helper launcher
src/epistemic_alignment/
  __init__.py                           Public version
  models.py                             Dataclasses shared by helper modules
  artifacts.py                          Manifest/front-matter/Gherkin loading
  validation.py                         Structural and traceability checks
  hashing.py                            Canonical hash projection
  review.py                             Readiness and approval-state operations
  handoff.py                            Approved Superpowers handoff rendering
  render.py                             Review-site JSON projection
  cli.py                                CLI argument parsing and exit codes
templates/alignment/                    Canonical target-project templates
skills/*/SKILL.md                       Eight method skills
skills/*/references/*.md                Focused method and artifact references
adapters/codex-site/template/           Sites-compatible vinext application
adapters/adapter-contract.md            Cross-harness renderer contract
adapters/{claude,opencode,qwen-code}.md Host-specific road maps
evals/cases/                            Skill scenario inputs and assertions
examples/approved-project/alignment/    Complete approved fixture
tests/                                  Python, plugin, skill, fixture, and CLI tests
```

---

### Task 1: Installable plugin skeleton and executable helper boundary

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `README.md`
- Create: `LICENSE`
- Create: `pyproject.toml`
- Create: `scripts/alignment`
- Create: `src/epistemic_alignment/__init__.py`
- Create: `src/epistemic_alignment/cli.py`
- Create: `tests/__init__.py`
- Create: `tests/test_plugin_package.py`

**Interfaces:**
- Consumes: the approved design specification.
- Produces: executable `scripts/alignment`; `python3 -m epistemic_alignment.cli`; plugin name `epistemic-alignment`; CLI exit code `0` for success, `1` for validation/readiness failure, and `2` for usage or unsupported-schema failure.

- [ ] **Step 1: Write failing package tests**

```python
# tests/test_plugin_package.py
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PluginPackageTests(unittest.TestCase):
    def test_manifest_exposes_skill_directory(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "alignment")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertEqual(manifest["skills"], "./skills/")

    def test_launcher_reports_version(self):
        result = subprocess.run(
            [str(ROOT / "scripts/alignment"), "--version"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "epistemic-alignment 0.1.0")
```

- [ ] **Step 2: Run the tests and confirm the skeleton is absent**

Run: `python3 -m unittest tests.test_plugin_package -v`

Expected: both tests fail because the manifest and launcher do not exist.

- [ ] **Step 3: Add the minimal manifest and CLI**

Use a valid Codex plugin manifest with `name: alignment`, display name `Epistemic Alignment`, `version`, `description`, `license`, `skills`, keywords, and interface fields. The manifest name preserves the designed `alignment:*` skill namespace; the GitHub repository can still be named `epistemic-alignment`. Do not add repository/homepage URLs before the GitHub remote exists.

```python
# src/epistemic_alignment/__init__.py
__version__ = "0.1.0"
```

`tests/__init__.py` inserts the repository `src/` directory at the front of `sys.path` so module-style test runs work without installing the package.

```python
# src/epistemic_alignment/cli.py
import argparse
from . import __version__


def build_parser():
    parser = argparse.ArgumentParser(prog="alignment")
    parser.add_argument("--version", action="version", version=f"epistemic-alignment {__version__}")
    return parser


def main(argv=None):
    build_parser().parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The launcher resolves the repository/plugin root relative to itself and prepends `src` to `PYTHONPATH` before executing `python3 -m epistemic_alignment.cli`.

- [ ] **Step 4: Make the launcher executable and run the tests**

Run: `chmod +x scripts/alignment`

Run: `python3 -m unittest tests.test_plugin_package -v`

Expected: 2 tests pass.

- [ ] **Step 5: Commit the skeleton**

```bash
git add .codex-plugin README.md LICENSE pyproject.toml scripts src tests/test_plugin_package.py
git commit -m "feat: scaffold epistemic alignment plugin"
```

---

### Task 2: Canonical templates and resumable initialization

**Files:**
- Create: `src/epistemic_alignment/models.py`
- Create: `src/epistemic_alignment/artifacts.py`
- Modify: `src/epistemic_alignment/cli.py`
- Create: `templates/alignment/manifest.yaml`
- Create: `templates/alignment/{charter,stakeholders,glossary,assumptions,open-questions}.md`
- Create: `templates/alignment/use-cases/.gitkeep`
- Create: `templates/alignment/features/.gitkeep`
- Create: `templates/alignment/architecture/{context,containers,components}.md`
- Create: `templates/alignment/decisions/.gitkeep`
- Create: `templates/alignment/review-state.json`
- Create: `tests/test_init.py`

**Interfaces:**
- Consumes: `Path target_root`, bundled templates.
- Produces: `initialize(target_root: Path, project_id: str, title: str) -> Path`; `load_artifact_set(alignment_dir: Path) -> ArtifactSet`; CLI `alignment init ROOT --project-id ID --title TITLE`.

- [ ] **Step 1: Write failing initialization tests**

```python
# tests/test_init.py
import json
import tempfile
import unittest
from pathlib import Path
from epistemic_alignment.artifacts import initialize, load_artifact_set


class InitializationTests(unittest.TestCase):
    def test_init_creates_parseable_resumable_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alignment_dir = initialize(root, "checkout", "Checkout redesign")
            artifacts = load_artifact_set(alignment_dir)
            self.assertEqual(artifacts.manifest["schema_version"], "1.0")
            self.assertEqual(artifacts.manifest["project"]["id"], "checkout")
            self.assertEqual(artifacts.manifest["current_phase"], "discover")
            state = json.loads((alignment_dir / "review-state.json").read_text())
            self.assertEqual(state["decision"]["value"], None)
            self.assertFalse((alignment_dir / "handoff.md").exists())

    def test_init_refuses_to_overwrite_existing_alignment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize(root, "checkout", "Checkout redesign")
            with self.assertRaises(FileExistsError):
                initialize(root, "other", "Other")
```

- [ ] **Step 2: Run the tests and confirm missing interfaces**

Run: `PYTHONPATH=src python3 -m unittest tests.test_init -v`

Expected: import failure for `epistemic_alignment.artifacts`.

- [ ] **Step 3: Implement models, JSON-compatible YAML loading, and template copy**

```python
# src/epistemic_alignment/models.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class Entity:
    id: str
    kind: str
    status: str
    priority: str
    source_kind: str
    source_ref: str
    confidence: str
    links: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class ArtifactSet:
    root: Path
    manifest: Dict[str, Any]
    entities: Dict[str, Entity]
    files: List[Path]
```

`manifest.yaml` is this JSON-compatible YAML document before project substitution:

```json
{
  "schema_version": "1.0",
  "project": {"id": "__PROJECT_ID__", "title": "__PROJECT_TITLE__"},
  "current_phase": "discover",
  "completed_phases": [],
  "artifacts": [
    "charter.md",
    "stakeholders.md",
    "glossary.md",
    "assumptions.md",
    "open-questions.md",
    "architecture/context.md",
    "architecture/containers.md",
    "architecture/components.md",
    "review-state.json"
  ],
  "renderer": {"adapter": null, "status": "not_generated", "location": null, "rendered_hash": null},
  "last_validation": null,
  "review_hash": null
}
```

Every initialized Markdown file uses JSON front matter between `---` delimiters. For example, `charter.md` starts with `{"artifact":"charter","entities":[]}` and then `# Charter`; the other files use their filename stem as the artifact value. Empty phase directories contain only `.gitkeep`, so initialization never invents a use case, scenario, or decision.

`review-state.json` starts as:

```json
{
  "schema_version": "1.0",
  "validation": {"status": "not_run", "blockers": [], "warnings": []},
  "presentation": {"status": "not_generated", "adapter": null, "location": null, "rendered_hash": null, "presented": false},
  "review": {"issued_hash": null, "issued_at": null},
  "decision": {"value": null, "reviewer": null, "provenance": null, "decided_at": null, "review_hash": null, "acknowledged_warnings": []},
  "handoff": {"verified_hash": null, "created_at": null}
}
```

Authored Gherkin files use stable-ID tags plus `# alignment-meta: {...}` records; initialization does not create a fake feature.

`initialize` copies templates, replaces only the project ID/title and initial phase fields, uses UTF-8/LF, and refuses overwrite.

- [ ] **Step 4: Add the `init` subcommand and run focused tests**

Run: `PYTHONPATH=src python3 -m unittest tests.test_init -v`

Expected: 2 tests pass.

Run: `scripts/alignment init /tmp/alignment-plan-smoke --project-id smoke --title "Smoke project"`

Expected: prints `/tmp/alignment-plan-smoke/alignment`; a second invocation exits nonzero and reports that the directory exists.

- [ ] **Step 5: Commit initialization**

```bash
git add src templates tests/test_init.py
git commit -m "feat: initialize canonical alignment artifacts"
```

---

### Task 3: Artifact parser and structural diagnostics

**Files:**
- Modify: `src/epistemic_alignment/models.py`
- Modify: `src/epistemic_alignment/artifacts.py`
- Create: `src/epistemic_alignment/validation.py`
- Modify: `src/epistemic_alignment/cli.py`
- Create: `tests/fixtures/valid-minimal/alignment/**`
- Create: `tests/fixtures/invalid-duplicates/alignment/**`
- Create: `tests/test_validation.py`

**Interfaces:**
- Consumes: initialized or authored canonical directory.
- Produces: `Diagnostic(code, severity, path, entity_id, message)`; `ValidationReport(valid, blockers, warnings, entities, coverage)`; `validate(alignment_dir: Path) -> ValidationReport`; CLI `alignment validate ROOT [--json]`.

- [ ] **Step 1: Write failing parser and duplicate-ID tests**

```python
# tests/test_validation.py
import unittest
from pathlib import Path
from epistemic_alignment.validation import validate

FIXTURES = Path(__file__).parent / "fixtures"


class ValidationTests(unittest.TestCase):
    def test_valid_minimal_fixture_parses_all_entity_families(self):
        report = validate(FIXTURES / "valid-minimal/alignment")
        self.assertTrue(report.valid, report.blockers)
        self.assertEqual(
            set(report.entities),
            {"GOAL-001", "STK-001", "UC-001", "SCN-001", "SYS-001", "CTR-001"},
        )

    def test_duplicate_id_is_a_blocker_with_both_paths(self):
        report = validate(FIXTURES / "invalid-duplicates/alignment")
        duplicate = [item for item in report.blockers if item.code == "duplicate-id"]
        self.assertEqual(len(duplicate), 1)
        self.assertIn("UC-001", duplicate[0].message)
        self.assertIn("use-cases", duplicate[0].message)
```

- [ ] **Step 2: Run focused tests and confirm they fail**

Run: `PYTHONPATH=src python3 -m unittest tests.test_validation -v`

Expected: failures because validation interfaces and fixtures are absent.

- [ ] **Step 3: Implement strict parsing and diagnostics**

```python
# additions to src/epistemic_alignment/models.py
@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str
    path: str
    entity_id: str
    message: str


@dataclass
class ValidationReport:
    valid: bool
    blockers: List[Diagnostic]
    warnings: List[Diagnostic]
    entities: Dict[str, Entity]
    coverage: Dict[str, Any]
```

Parser rules are exact:

- supported `schema_version` is `1.0` only;
- entity IDs match `^(GOAL|STK|ASM|Q|UC|SCN|SYS|CTR|CMP|ADR)-[0-9]{3}$`;
- status is one of `proposed`, `confirmed`, `rejected`, `superseded`;
- priority is one of `critical`, `high`, `medium`, `low`;
- source kind is one of `human`, `repository`, `external`, `agent_inference`;
- confidence is one of `high`, `medium`, `low`;
- every entity record has all epistemic fields and a links object;
- duplicate IDs, malformed JSON/YAML subset, unsupported versions, missing required files, and invalid enum values are blockers;
- superseded IDs remain addressable but do not count toward active coverage.

- [ ] **Step 4: Add CLI JSON output and run tests**

Run: `PYTHONPATH=src python3 -m unittest tests.test_validation -v`

Expected: all structural tests pass.

Run: `scripts/alignment validate tests/fixtures/invalid-duplicates --json`

Expected: exit `1` and JSON contains `"code": "duplicate-id"`.

- [ ] **Step 5: Commit parser and structural validation**

```bash
git add src tests/fixtures tests/test_validation.py
git commit -m "feat: validate canonical alignment structure"
```

---

### Task 4: Traceability and readiness coverage

**Files:**
- Modify: `src/epistemic_alignment/validation.py`
- Create: `tests/fixtures/invalid-traceability/alignment/**`
- Create: `tests/fixtures/blocked-unknown/alignment/**`
- Create: `tests/test_traceability.py`

**Interfaces:**
- Consumes: active `Entity` objects and their typed links.
- Produces: `calculate_coverage(entities) -> dict`; blocker codes `broken-reference`, `goal-without-stakeholder`, `goal-without-use-case`, `use-case-without-scenario`, `scenario-without-owner`, `critical-open-question`, and `critical-proposed-assumption`.

- [ ] **Step 1: Write failing invariant tests**

```python
# tests/test_traceability.py
import unittest
from pathlib import Path
from epistemic_alignment.validation import validate

FIXTURES = Path(__file__).parent / "fixtures"


class TraceabilityTests(unittest.TestCase):
    def test_priority_chain_requires_goal_to_c4_ownership(self):
        report = validate(FIXTURES / "invalid-traceability/alignment")
        codes = {item.code for item in report.blockers}
        self.assertEqual(
            codes,
            {"goal-without-use-case", "use-case-without-scenario", "scenario-without-owner"},
        )

    def test_critical_unknowns_block_readiness(self):
        report = validate(FIXTURES / "blocked-unknown/alignment")
        codes = {item.code for item in report.blockers}
        self.assertIn("critical-open-question", codes)
        self.assertIn("critical-proposed-assumption", codes)

    def test_valid_fixture_reports_complete_priority_coverage(self):
        report = validate(FIXTURES / "valid-minimal/alignment")
        self.assertEqual(report.coverage["priority_goals"], {"covered": 1, "total": 1})
        self.assertEqual(report.coverage["priority_use_cases"], {"covered": 1, "total": 1})
        self.assertEqual(report.coverage["software_scenarios"], {"owned": 1, "total": 1})
```

- [ ] **Step 2: Run tests and confirm missing invariant failures**

Run: `PYTHONPATH=src python3 -m unittest tests.test_traceability -v`

Expected: failures because coverage and traceability checks are absent.

- [ ] **Step 3: Implement typed-link rules**

Required link keys are:

```python
REQUIRED_LINKS = {
    "GOAL": {"stakeholders", "use_cases"},
    "UC": {"goals", "stakeholders", "scenarios"},
    "SCN": {"goals", "use_cases", "owners"},
    "ADR": {"goals", "scenarios", "elements"},
}
```

Treat `critical` and `high` as priority entities. Validate both directions where both fields exist, but report a single diagnostic per missing semantic edge. Component and ADR links are conditional; system/container ownership is sufficient for a scenario, and an ADR is required only when an active ADR claims the affected element or the artifact explicitly marks a decision as material.

- [ ] **Step 4: Run traceability and regression tests**

Run: `PYTHONPATH=src python3 -m unittest tests.test_traceability tests.test_validation -v`

Expected: all tests pass and diagnostics remain deterministic by `(path, entity_id, code)` ordering.

- [ ] **Step 5: Commit traceability**

```bash
git add src/epistemic_alignment/validation.py tests/fixtures tests/test_traceability.py
git commit -m "feat: enforce alignment traceability"
```

---

### Task 5: Deterministic content hashing and stale-review detection

**Files:**
- Create: `src/epistemic_alignment/hashing.py`
- Modify: `src/epistemic_alignment/cli.py`
- Create: `tests/test_hashing.py`

**Interfaces:**
- Consumes: canonical directory with supported manifest.
- Produces: `content_hash(alignment_dir: Path) -> HashResult(algorithm, digest, files)`; CLI `alignment hash ROOT [--json]`; algorithm label `sha256-v1`.

- [ ] **Step 1: Write failing normalization tests**

```python
# tests/test_hashing.py
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from epistemic_alignment.hashing import content_hash

FIXTURE = Path(__file__).parent / "fixtures/valid-minimal/alignment"


class HashingTests(unittest.TestCase):
    def test_process_state_and_line_endings_do_not_change_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            left = Path(directory) / "left"
            right = Path(directory) / "right"
            shutil.copytree(FIXTURE, left)
            shutil.copytree(FIXTURE, right)
            state = json.loads((right / "review-state.json").read_text())
            state["decision"]["value"] = "approved"
            (right / "review-state.json").write_text(json.dumps(state))
            charter = (right / "charter.md").read_text()
            (right / "charter.md").write_bytes(charter.replace("\n", "\r\n").encode())
            self.assertEqual(content_hash(left).digest, content_hash(right).digest)

    def test_semantic_change_changes_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "copy"
            shutil.copytree(FIXTURE, copy)
            before = content_hash(copy).digest
            charter = copy / "charter.md"
            charter.write_text(charter.read_text().replace("Complete checkout", "Complete secure checkout"))
            self.assertNotEqual(before, content_hash(copy).digest)
```

- [ ] **Step 2: Run tests and confirm the module is absent**

Run: `PYTHONPATH=src python3 -m unittest tests.test_hashing -v`

Expected: import failure for `epistemic_alignment.hashing`.

- [ ] **Step 3: Implement `sha256-v1` projection**

Hash these inputs in sorted POSIX-path order:

1. manifest projection containing only `schema_version`, `project`, and sorted `artifacts` paths;
2. every declared canonical artifact except `manifest.yaml`, `review-state.json`, and `handoff.md`;
3. path, a NUL byte, normalized UTF-8 file content, and a final NUL byte for every entry.

Normalize CRLF/CR to LF and reject invalid UTF-8. Do not normalize prose whitespace because formatting was part of the presented review.

```python
@dataclass(frozen=True)
class HashResult:
    algorithm: str
    digest: str
    files: List[str]
```

- [ ] **Step 4: Add CLI output and run tests twice**

Run: `PYTHONPATH=src python3 -m unittest tests.test_hashing -v`

Expected: 2 tests pass.

Run: `scripts/alignment hash tests/fixtures/valid-minimal --json`

Expected: stable JSON with `algorithm`, 64-character `digest`, and sorted `files` on both invocations.

- [ ] **Step 5: Commit hashing**

```bash
git add src/epistemic_alignment/hashing.py src/epistemic_alignment/cli.py tests/test_hashing.py
git commit -m "feat: hash reviewed alignment content"
```

---

### Task 6: Review state, human-only approval, and Superpowers handoff

**Files:**
- Create: `src/epistemic_alignment/review.py`
- Create: `src/epistemic_alignment/handoff.py`
- Modify: `src/epistemic_alignment/cli.py`
- Create: `tests/fixtures/approved/alignment/**`
- Create: `tests/test_approval.py`
- Create: `tests/test_handoff.py`

**Interfaces:**
- Consumes: validation report, current hash, review presentation record, explicit decision arguments.
- Produces: `issue_review`, `record_decision`, `check_readiness`, `write_handoff`; CLI subcommands `issue-review`, `decide`, `readiness`, and `handoff`.

- [ ] **Step 1: Write failing gate tests**

```python
# tests/test_approval.py
import shutil
import tempfile
import unittest
from pathlib import Path
from epistemic_alignment.review import issue_review, record_decision, check_readiness

FIXTURE = Path(__file__).parent / "fixtures/valid-minimal/alignment"


class ApprovalTests(unittest.TestCase):
    def test_agent_provenance_cannot_approve(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "alignment"
            shutil.copytree(FIXTURE, target)
            issued = issue_review(target, "codex-sites", "site://draft", presented=True)
            with self.assertRaisesRegex(ValueError, "human-message"):
                record_decision(target, "approved", "reviewer", "agent-inference", issued.digest, [])

    def test_stale_hash_blocks_handoff_readiness(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "alignment"
            shutil.copytree(FIXTURE, target)
            issued = issue_review(target, "codex-sites", "site://draft", presented=True)
            record_decision(target, "approved", "owner", "human-message", issued.digest, [])
            charter = target / "charter.md"
            charter.write_text(charter.read_text() + "\nChanged after review.\n")
            readiness = check_readiness(target)
            self.assertFalse(readiness.ready)
            self.assertIn("stale-approval", {item.code for item in readiness.blockers})
```

```python
# tests/test_handoff.py
import shutil
import tempfile
import unittest
from pathlib import Path
from epistemic_alignment.handoff import write_handoff

APPROVED = Path(__file__).parent / "fixtures/approved/alignment"


class HandoffTests(unittest.TestCase):
    def test_handoff_contains_hash_and_superpowers_entrypoint(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "alignment"
            shutil.copytree(APPROVED, target)
            result = write_handoff(target)
            text = result.read_text()
            self.assertIn("sha256-v1:", text)
            self.assertIn("superpowers:brainstorming", text)
            self.assertIn("Critical open questions: 0", text)
```

- [ ] **Step 2: Run gate tests and confirm missing modules**

Run: `PYTHONPATH=src python3 -m unittest tests.test_approval tests.test_handoff -v`

Expected: import failures for `review` and `handoff`.

- [ ] **Step 3: Implement the fail-closed state transitions**

`issue_review` requires structural validation to pass, writes the current hash into `review.issued_hash` and `presentation.rendered_hash`, and clears any prior decision. `record_decision` accepts only the three specified decisions, requires matching current/issued/rendered hashes, and accepts `approved` only with provenance `human-message`, `presented == true`, and an acknowledgement for every current warning code. `check_readiness` re-runs validation and hashing on every call.

The generated `handoff.md` contains project title, issued hash, confirmed goals, priority use cases, BDD coverage, C4 ownership, ADR list, acknowledged warnings, canonical file index, and the explicit next instruction: invoke `superpowers:brainstorming` with this file as required context.

- [ ] **Step 4: Run all helper tests and CLI negative cases**

Run: `PYTHONPATH=src python3 -m unittest discover -s tests -v`

Expected: all tests pass.

Run: `scripts/alignment handoff tests/fixtures/blocked-unknown`

Expected: exit `1`, no `handoff.md`, and blocker codes name the critical unknowns.

- [ ] **Step 5: Commit the approval gate**

```bash
git add src tests
git commit -m "feat: gate Superpowers handoff on human approval"
```

---

### Task 7: Author the portable alignment skill suite

**Files:**
- Create: `skills/align-project/SKILL.md`
- Create: `skills/discover-domain/SKILL.md`
- Create: `skills/write-use-cases/SKILL.md`
- Create: `skills/specify-behavior/SKILL.md`
- Create: `skills/model-architecture/SKILL.md`
- Create: `skills/verify-alignment/SKILL.md`
- Create: `skills/build-review/SKILL.md`
- Create: `skills/approve-handoff/SKILL.md`
- Create: `skills/shared/references/{artifact-contract,cockburn,bdd,c4,approval,platform-detection}.md`
- Create: `tests/test_skills.py`

**Interfaces:**
- Consumes: helper CLI and canonical templates.
- Produces: eight discoverable Codex skills; every method skill reads the shared artifact contract and names its exact canonical output; `align-project` hands off only through `approve-handoff`.

- [ ] **Step 1: Invoke `superpowers:writing-skills` and write failing structural tests**

The implementation turn for this task must read and follow `superpowers:writing-skills` before authoring any `SKILL.md`.

```python
# tests/test_skills.py
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "align-project", "discover-domain", "write-use-cases", "specify-behavior",
    "model-architecture", "verify-alignment", "build-review", "approve-handoff",
}


class SkillTests(unittest.TestCase):
    def test_exact_skill_set_has_valid_frontmatter(self):
        found = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(found, EXPECTED)
        for name in found:
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            self.assertRegex(text, rf"(?s)^---\nname: {re.escape(name)}\n.*?\n---\n")

    def test_approval_skill_contains_non_bypassable_human_gate(self):
        text = (ROOT / "skills/approve-handoff/SKILL.md").read_text()
        for phrase in ["human-message", "current content hash", "never self-approve", "superpowers:brainstorming"]:
            self.assertIn(phrase, text)

    def test_orchestrator_names_every_phase_and_resume_check(self):
        text = (ROOT / "skills/align-project/SKILL.md").read_text()
        for phase in ["qualify", "discover", "use_cases", "behavior", "architecture", "cross_check", "review", "decision", "handoff"]:
            self.assertIn(phase, text)
        self.assertIn("validate the manifest before resuming", text)
```

- [ ] **Step 2: Run tests and confirm skill directories are absent**

Run: `python3 -m unittest tests.test_skills -v`

Expected: failures for missing skill set.

- [ ] **Step 3: Author shared references and phase skills**

Each skill front matter has only `name` and a trigger-focused `description`. Each body contains:

- hard boundaries and forbidden behavior;
- required inputs and exact outputs;
- the helper command resolved relative to the plugin root;
- one-question-at-a-time stakeholder interaction where needed;
- phase completion criteria;
- restart behavior;
- the next skill transition.

Method references encode the templates agreed in the spec. The approval reference states the trust boundary verbatim and prohibits treating silence, prior generic permission, agent confidence, or a file edit as an explicit approval message.

- [ ] **Step 4: Run skill structure tests and manual link audit**

Run: `python3 -m unittest tests.test_skills -v`

Expected: all tests pass.

Run: `rg -n "skills/shared|scripts/alignment|alignment/|superpowers:" skills`

Expected: every referenced relative file exists, and only `approve-handoff` directs the workflow into Superpowers.

- [ ] **Step 5: Commit skills**

```bash
git add skills tests/test_skills.py
git commit -m "feat: add epistemic alignment skill suite"
```

---

### Task 8: Deterministic review-data projection and adapter contract

**Files:**
- Create: `src/epistemic_alignment/render.py`
- Modify: `src/epistemic_alignment/cli.py`
- Create: `adapters/adapter-contract.md`
- Create: `adapters/{claude,opencode,qwen-code}.md`
- Create: `tests/test_render_projection.py`

**Interfaces:**
- Consumes: valid canonical artifacts and current hash.
- Produces: `build_review_model(alignment_dir: Path) -> dict`; CLI `alignment render-data ROOT --output PATH`; adapter result fields `adapter`, `version`, `location`, `status`, `rendered_hash`, `warnings`.

- [ ] **Step 1: Write failing projection tests**

```python
# tests/test_render_projection.py
import unittest
from pathlib import Path
from epistemic_alignment.render import build_review_model

FIXTURE = Path(__file__).parent / "fixtures/valid-minimal/alignment"


class RenderProjectionTests(unittest.TestCase):
    def test_projection_contains_all_seven_review_views(self):
        model = build_review_model(FIXTURE)
        self.assertEqual(
            set(model),
            {"project", "summary", "stakeholders", "useCases", "behavior", "architecture", "decisions", "risks", "readiness", "reviewHash"},
        )
        self.assertEqual(model["reviewHash"]["algorithm"], "sha256-v1")

    def test_uncertainty_and_provenance_survive_projection(self):
        model = build_review_model(FIXTURE)
        goal = model["summary"]["goals"][0]
        self.assertIn("status", goal)
        self.assertIn("confidence", goal)
        self.assertIn("source_kind", goal)
```

- [ ] **Step 2: Run tests and confirm the projection is absent**

Run: `PYTHONPATH=src python3 -m unittest tests.test_render_projection -v`

Expected: import failure for `epistemic_alignment.render`.

- [ ] **Step 3: Implement the renderer-neutral model and adapter docs**

The projection must sort every entity list by stable ID, preserve links and epistemic metadata, include raw Mermaid/C4 source plus parsed ownership, and expose blockers separately from warnings. It must not include approval controls or mutate `review-state.json`.

The adapter contract documents exact input/result JSON fields, draft/presented/published states, hash equality, external-state consent, and failure isolation. Host road maps state:

- Claude renders the JSON as an Artifact and returns an Artifact reference;
- OpenCode writes a local static site and starts an explicit local preview command;
- Qwen Code reuses the static renderer and supplies Qwen extension/skill metadata.

- [ ] **Step 4: Run projection and full helper tests**

Run: `PYTHONPATH=src python3 -m unittest tests.test_render_projection -v`

Expected: 2 tests pass.

Run: `scripts/alignment render-data tests/fixtures/valid-minimal --output /tmp/alignment-review-data.json`

Expected: valid deterministic JSON containing the current hash and no decision mutation.

- [ ] **Step 5: Commit the adapter boundary**

```bash
git add src adapters tests/test_render_projection.py
git commit -m "feat: project alignment data for review adapters"
```

---

### Task 9: Codex ChatGPT Sites review application

**Files:**
- Create: `adapters/codex-site/template/.openai/hosting.json`
- Create: `adapters/codex-site/template/package.json`
- Create: `adapters/codex-site/template/pnpm-lock.yaml`
- Create: `adapters/codex-site/template/vite.config.ts`
- Create: `adapters/codex-site/template/next.config.ts`
- Create: `adapters/codex-site/template/tsconfig.json`
- Create: `adapters/codex-site/template/next-env.d.ts`
- Create: `adapters/codex-site/template/postcss.config.mjs`
- Create: `adapters/codex-site/template/eslint.config.mjs`
- Create: `adapters/codex-site/template/worker/index.ts`
- Create: `adapters/codex-site/template/app/layout.tsx`
- Create: `adapters/codex-site/template/app/page.tsx`
- Create: `adapters/codex-site/template/app/globals.css`
- Create: `adapters/codex-site/template/components/{Shell,StatusBadge,Traceability,C4Diagram,RiskPanel}.tsx`
- Create: `adapters/codex-site/template/lib/{schema,load-review}.ts`
- Create: `adapters/codex-site/template/public/alignment-review.json`
- Create: `adapters/codex-site/template/tests/rendered-html.test.mjs`
- Create: `tests/test_codex_site_adapter.py`
- Modify: `skills/build-review/SKILL.md`

**Interfaces:**
- Consumes: `alignment render-data` output matching `ReviewModel`.
- Produces: buildable Sites project at target `alignment-review/site`; seven navigable sections; visible provenance/uncertainty/blockers; returned adapter status with rendered hash.

- [ ] **Step 1: Invoke `sites:sites-building` and write failing adapter tests**

This task's implementation turn must read and follow the current `sites:sites-building` skill before creating the project. Use its vinext starter and remove unused persistence/auth code because v1 is presentational.

```python
# tests/test_codex_site_adapter.py
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "adapters/codex-site/template"


class CodexSiteAdapterTests(unittest.TestCase):
    def test_sites_manifest_is_presentational(self):
        hosting = json.loads((SITE / ".openai/hosting.json").read_text())
        self.assertEqual(hosting, {"d1": None, "r2": None})

    def test_review_fixture_matches_current_projection_shape(self):
        data = json.loads((SITE / "public/alignment-review.json").read_text())
        self.assertIn("reviewHash", data)
        self.assertIn("readiness", data)
        self.assertNotIn("approveAction", data)
```

- [ ] **Step 2: Run tests and confirm the Site does not exist**

Run: `python3 -m unittest tests.test_codex_site_adapter -v`

Expected: failures for missing hosting and review-data files.

- [ ] **Step 3: Build the presentational Sites template**

Pin React `19.2.6`, React DOM `19.2.6`, vinext `1.0.0-beta.2`, TypeScript `5.9.3`, and Mermaid `11.17.2`. `ReviewModel` mirrors Task 8 exactly. The page renders these anchored sections: `summary`, `stakeholders`, `use-cases`, `behavior`, `architecture`, `decisions-risks`, and `readiness`.

`StatusBadge` maps `confirmed/high` to a labeled solid state, `proposed/medium` to a labeled caution state, and `rejected/low` to a labeled critical state; color is never the only signal. `C4Diagram` renders Mermaid client-side and exposes the source in an expandable text panel. `Traceability` renders ID-linked chains. `RiskPanel` keeps blockers above warnings. No component can write approval state.

Update `build-review` so Codex detection runs `render-data`, copies the committed template to `alignment-review/site`, replaces `public/alignment-review.json`, uses Sites for build/inspection, and asks for consent before hosting.

- [ ] **Step 4: Run application checks and visual inspection**

Prepare the bundled toolchain for this workspace:

```bash
export PATH=/Users/darasokolovskaa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin:/Users/darasokolovskaa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback:$PATH
```

Run: `pnpm --dir adapters/codex-site/template install --frozen-lockfile`

Run: `pnpm --dir adapters/codex-site/template test`

Run: `pnpm --dir adapters/codex-site/template lint`

Expected: production build, rendered-HTML test, and lint all pass. Start the dev server, inspect representative desktop and narrow viewports, and save screenshots under `artifacts/site-qa/`; verify keyboard navigation, headings, contrast, hash visibility, uncertainty labels, and blocker prominence.

- [ ] **Step 5: Commit the Codex Site adapter**

```bash
git add adapters/codex-site skills/build-review tests/test_codex_site_adapter.py artifacts/site-qa
git commit -m "feat: render alignment reviews with ChatGPT Sites"
```

---

### Task 10: Scenario eval corpus and approval-gate behavioral checks

**Files:**
- Create: `evals/README.md`
- Create: `evals/cases/{greenfield,existing-repo,conflict,critical-unknown,bounded-skip,stale-approval}.md`
- Create: `evals/expected/*.json`
- Create: `scripts/check-evals`
- Create: `tests/test_eval_cases.py`
- Create: `artifacts/evals/results.json`

**Interfaces:**
- Consumes: installed plugin skills, six prompts, canonical expected assertions.
- Produces: normalized eval records with `case`, `artifacts`, `required`, `forbidden`, `gate`, and `evidence`; aggregate pass/fail report.

- [ ] **Step 1: Write failing eval-corpus tests**

```python
# tests/test_eval_cases.py
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = {"greenfield", "existing-repo", "conflict", "critical-unknown", "bounded-skip", "stale-approval"}


class EvalCorpusTests(unittest.TestCase):
    def test_every_case_has_machine_readable_assertions(self):
        cases = {path.stem for path in (ROOT / "evals/cases").glob("*.md")}
        expected = {path.stem for path in (ROOT / "evals/expected").glob("*.json")}
        self.assertEqual(cases, NAMES)
        self.assertEqual(expected, NAMES)
        for name in NAMES:
            assertion = json.loads((ROOT / f"evals/expected/{name}.json").read_text())
            self.assertTrue(assertion["required"])
            self.assertTrue(assertion["forbidden"])
            self.assertIn(assertion["gate"], {"blocked", "approved", "skipped", "invalidated"})
```

- [ ] **Step 2: Run tests and confirm corpus is absent**

Run: `python3 -m unittest tests.test_eval_cases -v`

Expected: failure because cases and assertions are missing.

- [ ] **Step 3: Author six bounded evals and the checker**

Every case includes a complete starting prompt, allowed repository evidence, scripted human answers, and stop condition. Expected JSON checks required files/IDs, forbidden silent confirmations, forbidden self-approval, expected gate state, and exact validator codes.

`scripts/check-evals RESULTS.json` verifies all assertions against captured artifact directories and transcript labels. The critical-unknown case must stop at `critical-open-question`; the conflict case must preserve both stakeholder positions; bounded-skip must record rationale and create no approval/handoff; stale-approval must remove or reject handoff readiness after mutation.

- [ ] **Step 4: Execute the cases against a clean plugin installation**

Install the working plugin through the Codex personal-plugin development workflow. Run each case in an isolated temporary fixture, capture canonical artifacts and relevant transcript evidence, then run:

Run: `scripts/check-evals artifacts/evals/results.json`

Expected: six cases pass; no forbidden behavior is observed. If the host cannot automate a transcript, perform the interaction manually and store the exact human/agent excerpts used as evidence in the result record.

- [ ] **Step 5: Commit eval evidence**

```bash
git add evals scripts/check-evals tests/test_eval_cases.py artifacts/evals/results.json
git commit -m "test: verify alignment skill behavior"
```

---

### Task 11: Clean installation, end-to-end example, and release documentation

**Files:**
- Modify: `README.md`
- Create: `docs/{installation,usage,recovery,trust-model,adapters}.md`
- Create: `examples/approved-project/alignment/**`
- Create: `examples/approved-project/alignment-review/site/**`
- Create: `tests/test_release.py`
- Create: `artifacts/release/e2e.json`
- Create: `artifacts/release/site-desktop.png`
- Create: `artifacts/release/site-narrow.png`

**Interfaces:**
- Consumes: completed helper, skills, Site adapter, Superpowers installation.
- Produces: installable v0.1.0 package, approved example, exact usage commands, recovery guide, adapter road map, and end-to-end evidence from request through Superpowers handoff.

- [ ] **Step 1: Write failing release checks**

```python
# tests/test_release.py
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleaseTests(unittest.TestCase):
    def test_docs_cover_install_use_recovery_trust_and_adapters(self):
        for name in ["installation", "usage", "recovery", "trust-model", "adapters"]:
            self.assertTrue((ROOT / f"docs/{name}.md").is_file(), name)

    def test_e2e_evidence_proves_verified_handoff(self):
        evidence = json.loads((ROOT / "artifacts/release/e2e.json").read_text())
        self.assertEqual(evidence["plugin_version"], "0.1.0")
        self.assertTrue(evidence["validation_passed"])
        self.assertTrue(evidence["site_presented"])
        self.assertTrue(evidence["human_approved"])
        self.assertEqual(evidence["review_hash"], evidence["handoff_hash"])
        self.assertTrue(evidence["superpowers_handoff_consumed"])
```

- [ ] **Step 2: Run release checks and confirm missing evidence**

Run: `python3 -m unittest tests.test_release -v`

Expected: failures for missing documentation and E2E evidence.

- [ ] **Step 3: Complete documentation and approved example**

Document:

- personal plugin installation and development reinstall/cache-buster flow;
- explicit and automatic skill invocation examples;
- all helper commands and exit codes;
- phase resumption and corrupt-artifact recovery;
- the non-cryptographic trust boundary;
- Site draft, inspection, consent, and publication behavior;
- Superpowers integration dependency;
- Claude Artifact, OpenCode local site, and Qwen Code local site adapter road maps.

The approved example must validate, contain a presented Codex Site projection, have a current human-message approval record, and generate `handoff.md` without manual edits.

- [ ] **Step 4: Perform clean-install E2E and full verification**

Use the Codex plugin development install flow from `plugin-creator`, restart/reload as required, and run a new complex-project interaction through all phases. Inspect the generated Site at desktop and narrow widths, explicitly approve the displayed hash, generate the handoff, and invoke Superpowers Brainstorming with it.

Run: `PYTHONPATH=src python3 -m unittest discover -s tests -v`

Run: `scripts/alignment validate examples/approved-project --json`

Run: `scripts/alignment readiness examples/approved-project --json`

Run: `pnpm --dir examples/approved-project/alignment-review/site test`

Expected: all suites pass; readiness is true; the Site build passes; `artifacts/release/e2e.json` records equal review/handoff hashes and consumed handoff.

- [ ] **Step 5: Commit release evidence**

```bash
git add README.md docs examples tests/test_release.py artifacts/release
git commit -m "docs: prepare Codex alignment plugin release"
```

---

### Task 12: Final audit and GitHub-ready repository state

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `README.md`
- Create: `.gitignore`
- Create: `CHANGELOG.md`
- Create: `artifacts/release/completion-audit.md`

**Interfaces:**
- Consumes: all release artifacts and the approved design specification.
- Produces: clean v0.1.0 repository, requirement-by-requirement completion audit, proposed GitHub repository metadata, and no unverified completion claims.

- [ ] **Step 1: Write the completion matrix before declaring success**

Create `artifacts/release/completion-audit.md` with one row for every explicit v1 scope item, workflow phase, artifact, gate invariant, adapter deliverable, test category, and release criterion in the design spec. Each row must link to authoritative file or command evidence and be marked `proven`, `contradicted`, or `missing`; `missing` or `contradicted` prevents release.

- [ ] **Step 2: Run repository hygiene and full verification**

Run: `git diff --check`

Run: `PYTHONPATH=src python3 -m unittest discover -s tests -v`

Run: `scripts/check-evals artifacts/evals/results.json`

Run: `pnpm --dir adapters/codex-site/template test`

Run: `git status --short`

Expected: no whitespace errors; all Python/eval/Site tests pass; only intentional completion-audit and release metadata changes remain.

- [ ] **Step 3: Resolve every non-proven audit row**

For each `missing` or `contradicted` row, either implement and verify the original requirement or leave the release incomplete. Do not weaken the requirement or rewrite the audit around existing behavior.

- [ ] **Step 4: Add GitHub-ready metadata without inventing a remote**

Add final keywords, screenshots, capabilities, changelog, generated-output ignores, and exact local verification commands. Record the recommended repository name `epistemic-alignment` and release tag `v0.1.0`. Add `repository` and homepage fields only after an actual GitHub remote exists.

- [ ] **Step 5: Commit the verified release state**

```bash
git add .codex-plugin/plugin.json README.md .gitignore CHANGELOG.md artifacts/release/completion-audit.md
git commit -m "chore: finalize epistemic alignment v0.1.0"
```

After this commit, rerun the full verification commands against `HEAD` and compare the completion audit to the original design spec before marking the active goal complete.
