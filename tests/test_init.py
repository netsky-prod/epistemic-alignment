import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from epistemic_alignment.artifacts import initialize, load_dossier


ROOT = Path(__file__).resolve().parents[1]


class InitializationTests(unittest.TestCase):
    def test_init_creates_thin_resumable_dossier(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alignment_dir = initialize(root, "checkout", "Checkout redesign")
            dossier = load_dossier(alignment_dir)
            self.assertEqual(dossier.manifest["schema_version"], "1.0")
            self.assertEqual(dossier.manifest["project"]["id"], "checkout")
            self.assertEqual(dossier.manifest["current_phase"], "discover")
            self.assertEqual(
                dossier.manifest["snapshot_paths"],
                dossier.snapshot_paths,
            )
            self.assertIn("review.md", dossier.snapshot_paths)
            state = json.loads((alignment_dir / "review-state.json").read_text())
            self.assertEqual(state["decision"], {})
            self.assertFalse((alignment_dir / "handoff.md").exists())

    def test_init_refuses_to_overwrite_existing_alignment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initialize(root, "checkout", "Checkout redesign")
            with self.assertRaises(FileExistsError):
                initialize(root, "other", "Other")

    def test_init_escapes_json_special_project_values(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project_id = 'checkout\\next\niteration'
            title = 'The "new" checkout\nredesign'
            dossier = load_dossier(initialize(root, project_id, title))
            self.assertEqual(dossier.manifest["project"]["id"], project_id)
            self.assertEqual(dossier.manifest["project"]["title"], title)

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
