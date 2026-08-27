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

    def test_manifest_exposes_final_release_discovery_metadata(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertGreaterEqual(
            set(manifest["keywords"]),
            {
                "alignment",
                "architecture",
                "bdd",
                "c4",
                "discovery",
                "human-approval",
                "requirements",
                "use-cases",
            },
        )
        self.assertEqual(manifest["interface"]["capabilities"], ["Interactive", "Write"])
        self.assertEqual(
            manifest["interface"]["screenshots"],
            ["./assets/site-desktop.png", "./assets/site-narrow.png"],
        )
        for relative_path in manifest["interface"]["screenshots"]:
            with self.subTest(relative_path=relative_path):
                screenshot = ROOT / relative_path.removeprefix("./")
                self.assertTrue(screenshot.is_file())
                self.assertEqual(screenshot.suffix, ".png")
                self.assertEqual(screenshot.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        for field in ["repository", "homepage"]:
            self.assertNotIn(field, manifest)
        self.assertNotIn("websiteURL", manifest["interface"])

    def test_launcher_reports_version(self):
        result = subprocess.run(
            [str(ROOT / "scripts/alignment"), "--version"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "epistemic-alignment 0.1.0")
