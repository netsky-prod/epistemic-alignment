import json
import os
import shutil
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


def run(*args, cwd=None, env=None):
    return subprocess.run(
        [str(arg) for arg in args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
    )


class ReleaseTests(unittest.TestCase):
    def test_every_directory_in_the_discoverable_skill_root_is_a_skill(self):
        skill_directories = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
        missing_manifests = [path.name for path in skill_directories if not (path / "SKILL.md").is_file()]
        self.assertEqual(missing_manifests, [])

    def test_required_docs_exist(self):
        for name in ["installation", "usage", "recovery", "trust-model", "adapters"]:
            with self.subTest(name=name):
                self.assertTrue((ROOT / f"docs/{name}.md").is_file(), name)

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
                [
                    "align-project",
                    "approve-handoff",
                    "build-review",
                    "discover-domain",
                    "model-architecture",
                    "review-alignment",
                    "specify-behavior",
                    "write-use-cases",
                ],
            )

            version = run(installed_plugin / "scripts/alignment", "--version", env=environment)
            self.assertEqual(version.returncode, 0, version.stderr)
            self.assertEqual(version.stdout.strip(), "epistemic-alignment 0.1.0")

            fixture = temporary / "fixture"
            initialized = run(
                installed_plugin / "scripts/alignment",
                "init",
                fixture,
                "--project-id",
                "clean-install-e2e",
                "--title",
                "Clean Install E2E",
                env=environment,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            snapshot = run(
                installed_plugin / "scripts/alignment",
                "snapshot",
                fixture,
                "--json",
                env=environment,
            )
            self.assertEqual(snapshot.returncode, 0, snapshot.stderr)
            self.assertEqual(json.loads(snapshot.stdout)["algorithm"], "sha256-v1")

    def test_release_evidence_binds_presented_site_to_approved_handoff(self):
        evidence = json.loads((ROOT / "artifacts/release/e2e.json").read_text())
        self.assertTrue(
            evidence["human_approved"],
            "release example awaits an explicit human approval of its issued hash",
        )
        self.assertTrue(
            evidence["superpowers_handoff_consumed"],
            "release example awaits a helper-generated handoff and Superpowers consumption",
        )
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

    def test_release_screenshots_exist(self):
        for name in ["site-desktop.png", "site-narrow.png"]:
            with self.subTest(name=name):
                screenshot = ROOT / "artifacts/release" / name
                self.assertTrue(screenshot.is_file(), name)
                self.assertGreater(screenshot.stat().st_size, 10_000, name)


if __name__ == "__main__":
    unittest.main()
