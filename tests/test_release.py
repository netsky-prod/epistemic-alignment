import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_CREATOR = Path(
    "/Users/darasokolovskaa/.codex/skills/.system/plugin-creator/scripts/create_basic_plugin.py"
)
PACKAGE_PATHS = (
    ".codex-plugin",
    "adapters",
    "references",
    "scripts",
    "skills",
    "src",
    "templates",
)
APPROVED_EXAMPLE = ROOT / "examples/approved-project"
APPROVED_DIGEST = "6394fafad6f9316d0082e6491c3626b52976780600323b90ec21bb3e19d07077"
APPROVED_FINDING = "FINDING-001"
EXPECTED_SKILLS = [
    "align-project",
    "approve-handoff",
    "build-review",
    "discover-domain",
    "model-architecture",
    "review-alignment",
    "specify-behavior",
    "write-use-cases",
]
REQUIRED_WORKFLOW_ARTIFACTS = (
    "alignment/manifest.yaml",
    "alignment/charter.md",
    "alignment/stakeholders.md",
    "alignment/glossary.md",
    "alignment/assumptions.md",
    "alignment/open-questions.md",
    "alignment/use-cases/UC-001.md",
    "alignment/features/release-handoff.feature",
    "alignment/architecture/context.md",
    "alignment/architecture/containers.md",
    "alignment/architecture/components.md",
    "alignment/decisions/ADR-001.md",
    "alignment/review.md",
    "alignment-review/site/.openai/hosting.json",
    "alignment-review/site/app/page.tsx",
    "alignment-review/site/components/C4Diagram.tsx",
    "alignment-review/site/components/FindingsPanel.tsx",
    "alignment-review/site/public/review.json",
    "alignment-review/site/tests/rendered-html.test.mjs",
)
INTAKE_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|$"
)


def run(*args, cwd=None, env=None):
    return subprocess.run(
        [str(arg) for arg in args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
    )


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_dimensions(path):
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise AssertionError(f"not a PNG with an IHDR chunk: {path}")
    return struct.unpack(">II", data[16:24])


class ReleaseTests(unittest.TestCase):
    def test_every_directory_in_the_discoverable_skill_root_is_a_skill(self):
        skill_directories = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
        missing_manifests = [path.name for path in skill_directories if not (path / "SKILL.md").is_file()]
        self.assertEqual(missing_manifests, [])

    def test_required_docs_exist(self):
        for name in ["installation", "usage", "recovery", "trust-model", "adapters"]:
            with self.subTest(name=name):
                self.assertTrue((ROOT / f"docs/{name}.md").is_file(), name)

    def test_github_ready_release_metadata_is_complete(self):
        readme = (ROOT / "README.md").read_text()
        changelog_path = ROOT / "CHANGELOG.md"
        self.assertTrue(changelog_path.is_file())
        changelog = changelog_path.read_text()
        self.assertIn("`epistemic-alignment`", readme)
        self.assertIn("`v0.1.0`", readme)
        self.assertIn("## 0.1.0 - 2026-08-27", changelog)
        for command in [
            "PYTHONPATH=src python3 -m unittest discover -s tests -v",
            "PYTHONPATH=src python3 -m unittest tests.test_release -v",
            "pnpm --dir adapters/codex-site/template test",
            "pnpm --dir examples/approved-project/alignment-review/site test",
        ]:
            with self.subTest(command=command):
                self.assertIn(command, readme)

    def test_agent_binds_a_simple_human_decision_to_the_issued_digest(self):
        usage = (ROOT / "docs/usage.md").read_text()
        approval_skill = (ROOT / "skills/approve-handoff/SKILL.md").read_text()
        for text in [usage, approval_skill]:
            with self.subTest(document=text[:40]):
                normalized = " ".join(text.split())
                self.assertIn("does not need to repeat or copy the digest", normalized)
                self.assertIn(
                    "binds that reply internally to the current issued digest", normalized
                )

    def test_clean_install_uses_packaged_plugin_in_isolated_codex_home(self):
        codex = shutil.which("codex")
        self.assertIsNotNone(codex, "codex CLI is required for the clean-install E2E")

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            marketplace = temporary / "marketplace"
            marketplace_json = marketplace / ".agents/plugins/marketplace.json"
            codex_home = temporary / "codex-home"
            isolated_home = temporary / "home"
            codex_home.mkdir()
            isolated_home.mkdir()

            scaffold = run(
                "python3",
                PLUGIN_CREATOR,
                "alignment",
                "--path",
                marketplace / "plugins",
                "--marketplace-path",
                marketplace_json,
                "--marketplace-name",
                "alignment-release-e2e",
                "--with-marketplace",
            )
            self.assertEqual(scaffold.returncode, 0, scaffold.stderr)

            packaged_plugin = marketplace / "plugins/alignment"
            shutil.rmtree(packaged_plugin)
            packaged_plugin.mkdir()
            for relative_path in PACKAGE_PATHS:
                source = ROOT / relative_path
                target = packaged_plugin / relative_path
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)

            environment = os.environ.copy()
            environment["CODEX_HOME"] = str(codex_home)
            environment["HOME"] = str(isolated_home)
            environment.pop("PYTHONPATH", None)

            add_marketplace = run(
                codex,
                "plugin",
                "marketplace",
                "add",
                marketplace,
                "--json",
                env=environment,
            )
            self.assertEqual(add_marketplace.returncode, 0, add_marketplace.stderr)
            install = run(
                codex,
                "plugin",
                "add",
                "alignment@alignment-release-e2e",
                "--json",
                env=environment,
            )
            self.assertEqual(install.returncode, 0, install.stderr)

            shutil.rmtree(marketplace)
            manifests = list(codex_home.glob("plugins/cache/**/alignment/**/.codex-plugin/plugin.json"))
            self.assertEqual(len(manifests), 1, manifests)
            installed_plugin = manifests[0].parents[1]
            self.assertEqual(
                sorted(path.parent.name for path in (installed_plugin / "skills").glob("*/SKILL.md")),
                EXPECTED_SKILLS,
            )

            version = run(installed_plugin / "scripts/alignment", "--version", env=environment)
            self.assertEqual(version.returncode, 0, version.stderr)
            self.assertEqual(version.stdout.strip(), "epistemic-alignment 0.1.0")

            fixture = temporary / "fixture"
            shutil.copytree(APPROVED_EXAMPLE / "alignment", fixture / "alignment")
            shutil.copytree(
                APPROVED_EXAMPLE / "alignment-review/site",
                fixture / "alignment-review/site",
                ignore=shutil.ignore_patterns(
                    ".next", ".vinext", ".wrangler", "dist", "node_modules"
                ),
            )
            for relative_path in REQUIRED_WORKFLOW_ARTIFACTS:
                with self.subTest(relative_path=relative_path):
                    self.assertTrue((fixture / relative_path).is_file(), relative_path)

            approved_state = json.loads((fixture / "alignment/review-state.json").read_text())
            self.assertEqual(approved_state["snapshot"]["digest"], APPROVED_DIGEST)
            self.assertEqual(approved_state["decision"]["decision"], "approved")
            self.assertEqual(approved_state["decision"]["reviewer"], "human stakeholder")
            self.assertEqual(approved_state["decision"]["provenance"], "human-message")
            self.assertEqual(approved_state["decision"]["review_hash"], APPROVED_DIGEST)
            self.assertEqual(
                approved_state["decision"]["acknowledged_findings"], [APPROVED_FINDING]
            )
            site = json.loads(
                (fixture / "alignment-review/site/public/review.json").read_text()
            )
            self.assertEqual(site["snapshot"]["digest"], APPROVED_DIGEST)

            snapshot = run(
                installed_plugin / "scripts/alignment",
                "snapshot",
                fixture,
                "--json",
                env=environment,
            )
            self.assertEqual(snapshot.returncode, 0, snapshot.stderr)
            snapshot_output = json.loads(snapshot.stdout)
            self.assertEqual(snapshot_output["digest"], APPROVED_DIGEST)

            issue = run(
                installed_plugin / "scripts/alignment",
                "issue-review",
                fixture,
                "--adapter",
                "codex-sites",
                "--status",
                "presented",
                "--location",
                "alignment-review/site",
                env=environment,
            )
            self.assertEqual(issue.returncode, 0, issue.stderr)

            decide = run(
                installed_plugin / "scripts/alignment",
                "decide",
                fixture,
                "--decision",
                "approved",
                "--reviewer",
                "human stakeholder",
                "--provenance",
                "human-message",
                "--review-hash",
                APPROVED_DIGEST,
                "--acknowledged-finding",
                APPROVED_FINDING,
                env=environment,
            )
            self.assertEqual(decide.returncode, 0, decide.stderr)

            check_before_handoff = run(
                installed_plugin / "scripts/alignment", "check", fixture, "--json", env=environment
            )
            self.assertEqual(check_before_handoff.returncode, 0, check_before_handoff.stderr)
            check_before_handoff_output = json.loads(check_before_handoff.stdout)
            self.assertTrue(check_before_handoff_output["ready"])

            handoff = run(
                installed_plugin / "scripts/alignment", "handoff", fixture, env=environment
            )
            self.assertEqual(handoff.returncode, 0, handoff.stderr)
            handoff_path = Path(handoff.stdout.strip())
            self.assertEqual(handoff_path, fixture / "alignment/handoff.md")
            self.assertIn(
                f"Approved snapshot: sha256-v1:{APPROVED_DIGEST}", handoff_path.read_text()
            )
            self.assertIn("superpowers:brainstorming", handoff_path.read_text())

            check_after_handoff = run(
                installed_plugin / "scripts/alignment", "check", fixture, "--json", env=environment
            )
            self.assertEqual(check_after_handoff.returncode, 0, check_after_handoff.stderr)
            check_after_handoff_output = json.loads(check_after_handoff.stdout)
            self.assertTrue(check_after_handoff_output["ready"])

            captured_outputs = {
                "snapshot": snapshot_output,
                "issue_review": issue.stdout.strip(),
                "decision": decide.stdout.strip(),
                "check_before_handoff": check_before_handoff_output,
                "handoff": str(handoff_path.relative_to(fixture)),
                "check_after_handoff": check_after_handoff_output,
            }
            evidence = json.loads((ROOT / "artifacts/release/e2e.json").read_text())
            mechanical_flow = evidence["clean_install"]["mechanical_flow"]
            self.assertEqual(mechanical_flow["fixture_source"], "examples/approved-project")
            self.assertEqual(
                mechanical_flow["command_sequence"],
                ["snapshot", "issue-review", "decide", "check", "handoff", "check"],
            )
            self.assertEqual(
                mechanical_flow["verified_artifacts"], list(REQUIRED_WORKFLOW_ARTIFACTS)
            )
            self.assertEqual(
                captured_outputs,
                mechanical_flow["captured_outputs"],
            )

    def test_release_evidence_binds_presented_site_to_approved_handoff(self):
        evidence = json.loads((ROOT / "artifacts/release/e2e.json").read_text())
        self.assertTrue(
            evidence["human_approved"],
            "release example awaits an explicit human approval of its issued hash",
        )
        self.assertNotIn("superpowers_handoff_consumed", evidence)
        self.assertEqual(evidence["superpowers_consumption"]["status"], "consumed")
        alignment = ROOT / "examples/approved-project/alignment"
        state = json.loads((alignment / "review-state.json").read_text())
        site = json.loads(
            (ROOT / "examples/approved-project/alignment-review/site/public/review.json").read_text()
        )
        snapshot_result = run(ROOT / "scripts/alignment", "snapshot", alignment, "--json")
        self.assertEqual(snapshot_result.returncode, 0, snapshot_result.stderr)
        current_hash = json.loads(snapshot_result.stdout)["digest"]

        self.assertEqual(evidence["plugin_version"], "0.1.0")
        self.assertTrue(evidence["site_presented"])
        self.assertFalse(evidence["semantic_validator_present"])
        self.assertEqual(
            {
                evidence["issued_hash"],
                evidence["rendered_hash"],
                evidence["approved_hash"],
                evidence["handoff_hash"],
                state["snapshot"]["digest"],
                state["presentation"]["rendered_hash"],
                state["decision"]["review_hash"],
                state["handoff"]["digest"],
                site["snapshot"]["digest"],
                current_hash,
            },
            {current_hash},
        )
        handoff = (alignment / "handoff.md").read_text()
        self.assertIn(f"Approved snapshot: sha256-v1:{current_hash}", handoff)

    def test_superpowers_intake_hashes_match_current_consumed_files(self):
        evidence = json.loads((ROOT / "artifacts/release/e2e.json").read_text())
        consumption = evidence["superpowers_consumption"]
        intake = ROOT / consumption["evidence_path"]
        self.assertEqual(sha256(intake), consumption["evidence_sha256"])

        rows = []
        for line in intake.read_text().splitlines():
            match = INTAKE_ROW.match(line)
            if match:
                rows.append((int(match.group(1)), match.group(2), match.group(3)))
        self.assertEqual([order for order, _, _ in rows], list(range(1, len(rows) + 1)))
        self.assertEqual(len(rows), consumption["consumed_source_count"])
        self.assertGreater(len(rows), 0)

        for _, relative_path, expected_hash in rows:
            with self.subTest(relative_path=relative_path):
                source = (ROOT / relative_path).resolve()
                source.relative_to(ROOT.resolve())
                self.assertTrue(source.is_file(), relative_path)
                self.assertEqual(sha256(source), expected_hash)

    def test_release_screenshot_metadata_matches_png_dimensions(self):
        evidence = json.loads((ROOT / "artifacts/release/e2e.json").read_text())
        for name in ["desktop", "narrow"]:
            with self.subTest(name=name):
                screenshot_evidence = evidence["visual_qa"][name]
                screenshot = ROOT / screenshot_evidence["path"]
                self.assertTrue(screenshot.is_file(), name)
                self.assertGreater(screenshot.stat().st_size, 10_000, name)
                width, height = png_dimensions(screenshot)
                self.assertEqual(
                    screenshot_evidence["png_pixels"], {"width": width, "height": height}
                )

    def test_completion_matrix_has_only_proven_rows_and_resolving_local_links(self):
        audit_path = ROOT / "artifacts/release/completion-audit.md"
        audit = audit_path.read_text(encoding="utf-8")
        rows = re.findall(
            r"^\|[^\n]*\|\s*(proven|contradicted|missing)\s*\|[^\n]*$",
            audit,
            flags=re.MULTILINE,
        )
        self.assertGreater(len(rows), 0)
        self.assertEqual(set(rows), {"proven"})

        local_links = []
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", audit):
            if "://" in target or target.startswith("#"):
                continue
            local_links.append(target)
            resolved = (audit_path.parent / target.split("#", 1)[0]).resolve()
            with self.subTest(target=target):
                self.assertTrue(resolved.exists(), target)
        self.assertGreater(len(local_links), 0)


if __name__ == "__main__":
    unittest.main()
