import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SITE = ROOT / "adapters/codex-site/template"


class CodexSiteTests(unittest.TestCase):
    def test_hosting_has_no_persistence_bindings(self):
        self.assertEqual(
            json.loads((SITE / ".openai/hosting.json").read_text()),
            {"d1": None, "r2": None},
        )

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
