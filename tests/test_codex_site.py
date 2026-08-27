import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SITE = ROOT / "adapters/codex-site/template"


class CodexSiteTests(unittest.TestCase):
    def test_hosting_has_no_persistence_bindings(self):
        hosting = json.loads((SITE / ".openai/hosting.json").read_text())
        self.assertEqual(hosting["d1"], None)
        self.assertEqual(hosting["r2"], None)
        self.assertLessEqual(set(hosting), {"project_id", "d1", "r2"})
        if "project_id" in hosting:
            self.assertIsInstance(hosting["project_id"], str)
            self.assertTrue(hosting["project_id"])

    def test_review_payload_is_presentational(self):
        data = json.loads((SITE / "public/review.json").read_text())
        self.assertEqual(
            set(data),
            {
                "project",
                "summary",
                "stakeholders",
                "useCases",
                "behavior",
                "architecture",
                "decisions",
                "risks",
                "findings",
                "snapshot",
            },
        )
        self.assertNotIn("approveAction", data)
        self.assertNotIn("decisionMutation", data)

    def test_every_summary_entry_names_a_dossier_source(self):
        data = json.loads((SITE / "public/review.json").read_text())
        entries = [data["project"], data["summary"], data["architecture"]]
        for key in ["goals"]:
            entries.extend(data["summary"][key])
        for key in ["stakeholders", "useCases", "behavior", "decisions", "risks", "findings"]:
            entries.extend(data[key])
        entries.extend(data["architecture"]["responsibilities"])

        for entry in entries:
            with self.subTest(entry=entry.get("id", entry.get("name", entry.get("title")))):
                self.assertRegex(entry.get("source", ""), r"^alignment/[^/].+")
                self.assertNotIn("..", entry["source"])


if __name__ == "__main__":
    unittest.main()
