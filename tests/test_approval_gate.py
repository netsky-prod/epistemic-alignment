import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from epistemic_alignment.approval import check_gate, issue_review, record_decision
from epistemic_alignment.handoff import write_handoff


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/alignment"


class ApprovalGateTests(unittest.TestCase):
    def dossier(self, directory):
        target = Path(directory) / "alignment"
        shutil.copytree(TEMPLATE, target)
        return target

    def state(self, target):
        return json.loads((target / "review-state.json").read_text(encoding="utf-8"))

    def test_unchanged_human_approved_presented_snapshot_can_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            issued = issue_review(target, "codex-sites", "presented", "site://review")
            record_decision(target, "approved", "owner", "human-message", issued.digest, [])

            self.assertTrue(check_gate(target).ready)
            handoff = write_handoff(target)

            content = handoff.read_text(encoding="utf-8")
            self.assertIn("sha256-v1:" + issued.digest, content)
            self.assertIn("review.md", content)
            self.assertIn("superpowers:brainstorming", content)

    def test_agent_provenance_and_unpresented_review_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            issued = issue_review(target, "codex-sites", "draft", "site://draft")

            with self.assertRaises(ValueError):
                record_decision(
                    target, "approved", "agent", "agent-inference", issued.digest, []
                )

    def test_post_approval_edit_blocks_and_refuses_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            issued = issue_review(target, "codex-sites", "presented", "site://review")
            record_decision(target, "approved", "owner", "human-message", issued.digest, [])
            (target / "review.md").write_text("changed", encoding="utf-8")

            gate = check_gate(target)
            self.assertFalse(gate.ready)
            self.assertIn("stale-approval", gate.reasons)
            with self.assertRaises(ValueError):
                write_handoff(target)
            self.assertEqual(self.state(target)["handoff"], {})

    def test_approval_requires_the_exact_issued_rendered_and_current_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            issued = issue_review(target, "codex-sites", "published", "site://review")

            with self.assertRaises(ValueError):
                record_decision(target, "approved", "owner", "human-message", "0" * 64, [])
            self.assertEqual(self.state(target)["decision"], {})

            state = self.state(target)
            state["presentation"]["rendered_hash"] = "f" * 64
            (target / "review-state.json").write_text(json.dumps(state), encoding="utf-8")
            gate = check_gate(target)
            self.assertFalse(gate.ready)
            self.assertIn("hash-mismatch", gate.reasons)

    def test_changes_requested_and_rejected_are_never_handoff_ready(self):
        for decision in ("changes_requested", "rejected"):
            with self.subTest(decision=decision), tempfile.TemporaryDirectory() as directory:
                target = self.dossier(directory)
                issued = issue_review(target, "codex-sites", "presented", "site://review")
                record_decision(target, decision, "owner", "human-message", issued.digest, ["F-1"])

                gate = check_gate(target)
                self.assertFalse(gate.ready)
                self.assertIn("decision-not-approved", gate.reasons)
                with self.assertRaises(ValueError):
                    write_handoff(target)

    def test_unissued_review_is_not_ready_with_a_specific_reason(self):
        with tempfile.TemporaryDirectory() as directory:
            gate = check_gate(self.dossier(directory))

            self.assertFalse(gate.ready)
            self.assertIn("review-not-issued", gate.reasons)

    def test_state_updates_preserve_unrelated_sections_and_clear_old_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            state = self.state(target)
            state["unrelated"] = {"keep": True}
            state["snapshot"] = {"foreign": "preserved"}
            state["handoff"] = {"old": "cleared"}
            (target / "review-state.json").write_text(json.dumps(state), encoding="utf-8")

            issued = issue_review(target, "codex-sites", "presented", "site://review")
            state = self.state(target)
            self.assertEqual(state["unrelated"], {"keep": True})
            self.assertEqual(state["snapshot"]["foreign"], "preserved")
            self.assertEqual(state["handoff"], {})

            record_decision(target, "approved", "owner", "human-message", issued.digest, ["F-1"])
            write_handoff(target)
            self.assertEqual(self.state(target)["unrelated"], {"keep": True})

    def test_cli_gate_commands_report_success_and_reject_invalid_decision(self):
        with tempfile.TemporaryDirectory() as directory:
            project_root = Path(directory) / "project"
            target = self.dossier(project_root)
            issue = subprocess.run(
                [
                    str(ROOT / "scripts/alignment"),
                    "issue-review",
                    str(target),
                    "--adapter",
                    "codex-sites",
                    "--status",
                    "presented",
                    "--location",
                    "site://review",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(issue.returncode, 0, issue.stderr)
            digest = issue.stdout.strip().split(":", 1)[1]

            invalid = subprocess.run(
                [
                    str(ROOT / "scripts/alignment"),
                    "decide",
                    str(target),
                    "--decision",
                    "not-a-decision",
                    "--reviewer",
                    "owner",
                    "--provenance",
                    "human-message",
                    "--review-hash",
                    digest,
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("unsupported decision", invalid.stderr)

            accepted = subprocess.run(
                [
                    str(ROOT / "scripts/alignment"),
                    "decide",
                    str(target),
                    "--decision",
                    "approved",
                    "--reviewer",
                    "owner",
                    "--provenance",
                    "human-message",
                    "--review-hash",
                    digest,
                    "--acknowledged-finding",
                    "F-1",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)

            check = subprocess.run(
                [str(ROOT / "scripts/alignment"), "check", str(target), "--json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(check.returncode, 0, check.stderr)
            self.assertTrue(json.loads(check.stdout)["ready"])


if __name__ == "__main__":
    unittest.main()
