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


if __name__ == "__main__":
    unittest.main()
