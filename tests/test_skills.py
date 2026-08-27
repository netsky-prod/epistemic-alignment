import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "align-project", "discover-domain", "write-use-cases", "specify-behavior",
    "model-architecture", "review-alignment", "build-review", "approve-handoff",
}


class SkillTests(unittest.TestCase):
    def test_exact_skill_set(self):
        found = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(found, EXPECTED)

    def test_each_skill_has_a_valid_trigger_and_interface(self):
        for name in EXPECTED:
            with self.subTest(name=name):
                skill = ROOT / "skills" / name
                text = (skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(f"name: {name}", text)
                self.assertRegex(text, r"description: Use when [^\n]+")
                self.assertTrue((skill / "agents" / "openai.yaml").is_file())

    def test_semantic_review_never_claims_machine_proof(self):
        text = (ROOT / "skills/review-alignment/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("human judgment", text)
        self.assertIn("review.md", text)
        for forbidden in ["the semantic validator passed", "coverage is complete", "architecture is correct"]:
            self.assertNotIn(forbidden, text.lower())

    def test_handoff_skill_has_explicit_human_and_hash_gate(self):
        text = (ROOT / "skills/approve-handoff/SKILL.md").read_text(encoding="utf-8")
        for phrase in ["explicit human message", "human-message", "current snapshot", "never self-approve", "superpowers:brainstorming"]:
            self.assertIn(phrase, text)

    def test_shared_method_references_exist(self):
        references = ROOT / "skills/shared/references"
        for name in ["artifact-contract", "cockburn", "bdd", "c4", "semantic-review", "approval", "platform-detection"]:
            self.assertTrue((references / f"{name}.md").is_file(), name)


if __name__ == "__main__":
    unittest.main()
