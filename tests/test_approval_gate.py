import json
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

import epistemic_alignment.handoff as handoff_module
import epistemic_alignment.approval as approval_module
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

    def approve(self, target):
        issued = issue_review(target, "codex-sites", "presented", "site://review")
        record_decision(target, "approved", "owner", "human-message", issued.digest, [])
        return issued

    def write_state(self, target, state):
        (target / "review-state.json").write_text(json.dumps(state), encoding="utf-8")

    def assert_no_handoff_transition_artifacts(self, target):
        self.assertFalse((target / ".handoff-backup").exists())
        self.assertEqual(list(target.glob(".handoff-backup-*")), [])
        self.assertEqual(list(target.glob(".handoff-*.tmp")), [])

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

            record_decision(target, "approved", "owner", "human-message", issued.digest, [])

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
            self.assertIn("review-state-invalid", gate.reasons)

    def test_missing_or_wrong_type_required_state_fields_fail_closed(self):
        invalid_fields = [
            ("snapshot", "algorithm", None),
            ("snapshot", "algorithm", "md5"),
            ("snapshot", "digest", None),
            ("snapshot", "paths", "review.md"),
            ("snapshot", "issued_at", 1),
            ("presentation", "adapter", 1),
            ("presentation", "status", "unknown"),
            ("presentation", "location", []),
            ("presentation", "rendered_hash", None),
            ("presentation", "presented_at", None),
            ("decision", "decision", "unknown"),
            ("decision", "reviewer", []),
            ("decision", "provenance", []),
            ("decision", "decided_at", None),
            ("decision", "review_hash", None),
            ("decision", "acknowledged_findings", [1]),
        ]
        for section, field, value in invalid_fields:
            with self.subTest(section=section, field=field), tempfile.TemporaryDirectory() as directory:
                target = self.dossier(directory)
                self.approve(target)
                state = self.state(target)
                state[section][field] = value
                self.write_state(target, state)

                gate = check_gate(target)
                self.assertFalse(gate.ready)
                self.assertEqual(gate.reasons, ["review-state-invalid"])

    def test_malformed_handoff_state_fails_closed_without_raising(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            write_handoff(target)
            state = self.state(target)
            state["handoff"]["verified_at"] = []
            self.write_state(target, state)

            gate = check_gate(target)
            self.assertFalse(gate.ready)
            self.assertEqual(gate.reasons, ["review-state-invalid"])

    def test_unsupported_handoff_algorithm_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            write_handoff(target)
            state = self.state(target)
            state["handoff"]["algorithm"] = "md5"
            self.write_state(target, state)

            gate = check_gate(target)
            self.assertFalse(gate.ready)
            self.assertEqual(gate.reasons, ["review-state-invalid"])

    def test_review_must_be_snapshotted_before_review_or_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            manifest = json.loads((target / "manifest.yaml").read_text(encoding="utf-8"))
            manifest["snapshot_paths"].remove("review.md")
            (target / "manifest.yaml").write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaises(ValueError):
                issue_review(target, "codex-sites", "presented", "site://review")
            gate = check_gate(target)
            self.assertFalse(gate.ready)
            self.assertIn("review-not-snapshotted", gate.reasons)
            with self.assertRaises(ValueError):
                write_handoff(target)

    def test_issuing_a_new_review_removes_the_previous_handoff_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            write_handoff(target)
            self.assertTrue((target / "handoff.md").exists())

            issue_review(target, "codex-sites", "presented", "site://replacement")

            self.assertFalse((target / "handoff.md").exists())
            self.assertEqual(self.state(target)["handoff"], {})

    def test_post_write_edit_removes_the_newly_stale_handoff_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            original_write = handoff_module._write_text_atomically

            def edit_after_write(path, content):
                original_write(path, content)
                (target / "review.md").write_text("edited during handoff", encoding="utf-8")

            with mock.patch.object(handoff_module, "_write_text_atomically", edit_after_write):
                with self.assertRaises(ValueError):
                    write_handoff(target)

            self.assertFalse((target / "handoff.md").exists())
            self.assertEqual(self.state(target)["handoff"], {})

    def test_post_state_write_edit_removes_the_newly_stale_handoff_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            original_write = handoff_module._write_state

            def edit_after_state_write(alignment_dir, state):
                original_write(alignment_dir, state)
                if state["handoff"]:
                    (target / "review.md").write_text(
                        "edited after handoff state", encoding="utf-8"
                    )

            with mock.patch.object(handoff_module, "_write_state", edit_after_state_write):
                with self.assertRaises(ValueError):
                    write_handoff(target)

            self.assertFalse((target / "handoff.md").exists())
            self.assertEqual(self.state(target)["handoff"], {})

    def test_concurrent_new_review_waits_for_handoff_then_removes_it(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            wrote_handoff = threading.Event()
            release_handoff = threading.Event()
            failures = []
            original_write = handoff_module._write_text_atomically

            def pause_after_write(path, content):
                original_write(path, content)
                wrote_handoff.set()
                self.assertTrue(release_handoff.wait(3))

            def capture(callable_):
                try:
                    callable_()
                except BaseException as error:
                    failures.append(error)

            with mock.patch.object(handoff_module, "_write_text_atomically", pause_after_write):
                handoff_thread = threading.Thread(target=capture, args=(lambda: write_handoff(target),))
                handoff_thread.start()
                self.assertTrue(wrote_handoff.wait(3))
                issue_thread = threading.Thread(
                    target=capture,
                    args=(lambda: issue_review(target, "codex-sites", "presented", "site://new"),),
                )
                issue_thread.start()
                self.assertTrue(issue_thread.is_alive())
                release_handoff.set()
                handoff_thread.join(3)
                issue_thread.join(3)

            self.assertFalse(handoff_thread.is_alive())
            self.assertFalse(issue_thread.is_alive())
            self.assertEqual(failures, [])
            self.assertFalse((target / "handoff.md").exists())
            self.assertFalse(check_gate(target).ready)

    def test_handoff_state_write_failure_removes_the_published_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            original_write = handoff_module._write_state
            failed = False

            def fail_handoff_state_once(alignment_dir, state):
                nonlocal failed
                if state["handoff"] and not failed:
                    failed = True
                    raise OSError("injected handoff state write failure")
                original_write(alignment_dir, state)

            with mock.patch.object(handoff_module, "_write_state", fail_handoff_state_once):
                with self.assertRaises(OSError):
                    write_handoff(target)

            self.assertFalse((target / "handoff.md").exists())
            self.assertEqual(self.state(target)["handoff"], {})
            self.assert_no_handoff_transition_artifacts(target)

    def test_issue_review_state_write_failure_restores_previous_handoff_and_state(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            handoff = write_handoff(target)
            old_content = handoff.read_text(encoding="utf-8")
            old_state = self.state(target)

            with mock.patch.object(
                approval_module,
                "_write_state",
                side_effect=OSError("injected issue state write failure"),
            ):
                with self.assertRaises(OSError):
                    issue_review(target, "codex-sites", "presented", "site://replacement")

            self.assertEqual(handoff.read_text(encoding="utf-8"), old_content)
            self.assertEqual(self.state(target), old_state)
            self.assert_no_handoff_transition_artifacts(target)

    def test_record_decision_state_write_failure_restores_previous_handoff_and_state(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            handoff = write_handoff(target)
            old_content = handoff.read_text(encoding="utf-8")
            old_state = self.state(target)

            with mock.patch.object(
                approval_module,
                "_write_state",
                side_effect=OSError("injected decision state write failure"),
            ):
                with self.assertRaises(OSError):
                    record_decision(
                        target,
                        "changes_requested",
                        "owner",
                        "human-message",
                        old_state["snapshot"]["digest"],
                        ["F-1"],
                    )

            self.assertEqual(handoff.read_text(encoding="utf-8"), old_content)
            self.assertEqual(self.state(target), old_state)
            self.assert_no_handoff_transition_artifacts(target)

    def test_unrestored_handoff_backup_fails_closed_and_blocks_new_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            write_handoff(target)

            with mock.patch.object(
                approval_module,
                "_write_state",
                side_effect=OSError("injected state write failure"),
            ), mock.patch.object(
                approval_module,
                "_restore_handoff",
                side_effect=OSError("injected rollback failure"),
            ):
                with self.assertRaises(OSError):
                    record_decision(
                        target,
                        "changes_requested",
                        "owner",
                        "human-message",
                        self.state(target)["snapshot"]["digest"],
                        ["F-1"],
                    )

            self.assertTrue((target / ".handoff-backup").exists())
            self.assertFalse((target / "handoff.md").exists())
            gate = check_gate(target)
            self.assertFalse(gate.ready)
            self.assertIn("handoff-transaction-unresolved", gate.reasons)
            with self.assertRaises(ValueError):
                write_handoff(target)
            self.assertTrue((target / ".handoff-backup").exists())

    def test_verified_handoff_state_requires_the_handoff_file_and_digest_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.dossier(directory)
            self.approve(target)
            handoff = write_handoff(target)
            digest = self.state(target)["handoff"]["digest"]

            handoff.unlink()
            gate = check_gate(target)
            self.assertFalse(gate.ready)
            self.assertIn("handoff-file-missing", gate.reasons)
            with self.assertRaises(ValueError):
                write_handoff(target)

            handoff.write_text("wrong handoff", encoding="utf-8")
            gate = check_gate(target)
            self.assertFalse(gate.ready)
            self.assertIn("handoff-digest-mismatch", gate.reasons)
            self.assertNotIn("sha256-v1:" + digest, handoff.read_text(encoding="utf-8"))

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
