import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAMES = {
    "greenfield",
    "existing-repo",
    "conflict",
    "critical-unknown",
    "bounded-skip",
    "stale-approval",
    "self-approval",
}


class EvalTests(unittest.TestCase):
    def test_cases_and_assertions_are_complete(self):
        self.assertEqual({p.stem for p in (ROOT / "evals/cases").glob("*.md")}, NAMES)
        self.assertEqual({p.stem for p in (ROOT / "evals/expected").glob("*.json")}, NAMES)
        for name in NAMES:
            expected = json.loads((ROOT / f"evals/expected/{name}.json").read_text())
            self.assertTrue(expected["required"])
            self.assertTrue(expected["forbidden"])
            self.assertIn(expected["gate"], {"approved", "blocked", "skipped", "invalidated"})

    def test_cases_state_the_reproducible_inputs_and_boundaries(self):
        required_headings = {
            "Starting prompt",
            "Available evidence",
            "Scripted human answers",
            "Expected dossier and Site behavior",
            "Forbidden claims",
            "Expected gate result",
        }
        for name in NAMES:
            with self.subTest(name=name):
                text = (ROOT / f"evals/cases/{name}.md").read_text(encoding="utf-8")
                for heading in required_headings:
                    self.assertIn("## " + heading, text)

    def test_checker_validates_captured_results_and_reexecutes_helper_cases(self):
        checker = ROOT / "scripts/check-evals"
        self.assertTrue(checker.is_file())
        self.assertTrue(checker.stat().st_mode & 0o111)
        result = subprocess.run(
            [str(checker), "artifacts/evals/results.json"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("7 cases passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
