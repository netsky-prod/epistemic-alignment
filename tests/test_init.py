import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from epistemic_alignment.artifacts import initialize, load_artifact_set


ROOT = Path(__file__).resolve().parents[1]


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

    def test_cli_initializes_requested_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            result = subprocess.run(
                [
                    str(ROOT / "scripts/alignment"),
                    "init",
                    str(root),
                    "--project-id",
                    "checkout",
                    "--title",
                    "Checkout redesign",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), str(root / "alignment"))
