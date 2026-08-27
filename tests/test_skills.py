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
        forbidden_claims = [
            " ".join(("the semantic", "validator passed")),
            "".join((
                "coverage is",
                " complete",
            )),
            " ".join(("architecture is", "correct")),
        ]
        for forbidden in forbidden_claims:
            self.assertNotIn(forbidden, text.lower())

    def test_handoff_skill_has_explicit_human_and_hash_gate(self):
        text = (ROOT / "skills/approve-handoff/SKILL.md").read_text(encoding="utf-8")
        for phrase in ["explicit human message", "human-message", "current snapshot", "never self-approve", "superpowers:brainstorming"]:
            self.assertIn(phrase, text)

    def test_shared_method_references_exist(self):
        references = ROOT / "references"
        for name in ["artifact-contract", "cockburn", "bdd", "c4", "semantic-review", "approval", "platform-detection"]:
            self.assertTrue((references / f"{name}.md").is_file(), name)

    def test_reviewable_artifacts_sync_snapshot_membership_at_every_stage(self):
        contract = (ROOT / "references/artifact-contract.md").read_text(encoding="utf-8")
        for phrase in [
            "mandatory snapshot membership invariant",
            "snapshot_paths",
            "created, renamed, or deleted",
            "use-cases/UC-*.md",
            "features/*.feature",
            "decisions/ADR-*.md",
            "review-state.json",
            "handoff.md",
        ]:
            self.assertIn(phrase, contract)

        producing = [
            "align-project", "discover-domain", "write-use-cases",
            "specify-behavior", "model-architecture", "review-alignment",
        ]
        issuing = ["review-alignment", "build-review", "approve-handoff"]
        for name in producing:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("sync manifest `snapshot_paths`", text.lower(), name)
        for name in issuing:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("verify every current reviewable dossier file is listed", text.lower(), name)

    def test_align_project_resume_mapping_has_one_dynamic_transition_marker(self):
        text = (ROOT / "skills/align-project/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("`discover` → `alignment:discover-domain`", text)
        self.assertIn("`use-cases` → `alignment:write-use-cases`", text)
        self.assertIn("`behavior` → `alignment:specify-behavior`", text)
        self.assertIn("`architecture` → `alignment:model-architecture`", text)
        self.assertIn("`review` → `alignment:review-alignment`", text)
        self.assertIn("`presentation` → `alignment:build-review`", text)
        self.assertIn("`approval` → `alignment:approve-handoff`", text)
        self.assertEqual(text.count("Next transition:"), 1)
        self.assertNotIn("Next transition: `alignment:discover-domain`", text)

    def test_approval_reference_uses_exact_cli_argument_order(self):
        text = (ROOT / "references/approval.md").read_text(encoding="utf-8")
        self.assertIn(
            "scripts/alignment decide <root> --decision approved --reviewer <label> --provenance human-message --review-hash <hash> --acknowledged-finding ID",
            text,
        )
        self.assertIn("scripts/alignment check <root>", text)
        self.assertIn("scripts/alignment handoff <root>", text)

    def test_handoff_skill_shows_repeatable_decision_finding_flags(self):
        text = (ROOT / "skills/approve-handoff/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "scripts/alignment decide <root> --decision approved --reviewer <label> --provenance human-message --review-hash <hash> --acknowledged-finding ID [--acknowledged-finding ID ...]",
            text,
        )

    def test_approve_handoff_preserves_verified_delivery_when_superpowers_is_unavailable(self):
        text = " ".join(
            (ROOT / "skills/approve-handoff/SKILL.md").read_text(encoding="utf-8").split()
        ).lower()
        for requirement in [
            "if `superpowers:brainstorming` is unavailable",
            "leave the verified `alignment/handoff.md` and approval state untouched",
            "delivery pending",
            "exact `alignment/handoff.md` path",
            "resume the transition when `superpowers:brainstorming` becomes available",
            "do not regenerate the handoff or mutate approval state",
        ]:
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_approve_handoff_checks_existing_handoff_before_normal_approval(self):
        text = (ROOT / "skills/approve-handoff/SKILL.md").read_text(encoding="utf-8")
        resume = text.index("## Pending Delivery Resume")
        normal_approval = text.index("## Normal Approval")
        self.assertLess(resume, normal_approval)

        branch = " ".join(text[resume:normal_approval].split()).lower()
        for requirement in [
            "if `alignment/handoff.md` exists",
            "scripts/alignment check <root> --json",
            "when the check returns `ready: true`",
            "do not ask for a decision",
            "do not run `scripts/alignment decide`",
            "do not run `scripts/alignment handoff`",
            "deliver the existing handoff and dossier",
            "when the check is not ready",
            "do not deliver",
            "return to presentation and reapproval",
        ]:
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, branch)

    def test_build_review_requires_working_internal_traceability_links(self):
        text = " ".join(
            (ROOT / "skills/build-review/SKILL.md").read_text(encoding="utf-8").split()
        ).lower()
        for requirement in [
            "working internal traceability links",
            "stable source-to-anchor mapping",
            "rendered evidence index",
            "every evidence href resolves",
            "raw dossier source text visible",
        ]:
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_each_skill_declares_one_input_output_boundary(self):
        for name in EXPECTED:
            with self.subTest(name=name):
                text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertEqual(text.count("Input:"), 1)
                self.assertEqual(text.count("Output:"), 1)


if __name__ == "__main__":
    unittest.main()
