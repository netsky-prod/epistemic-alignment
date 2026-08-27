import json
import shutil
import subprocess
import tempfile
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
RUN_KINDS = {
    "greenfield": "dossier-run",
    "existing-repo": "dossier-run",
    "conflict": "dossier-run",
    "critical-unknown": "dossier-run",
    "bounded-skip": "bounded-skip-run",
    "stale-approval": "deterministic-fixture",
    "self-approval": "deterministic-fixture",
}


class EvalTests(unittest.TestCase):
    def run_checker(self, results_path):
        return subprocess.run(
            [str(ROOT / "scripts/check-evals"), str(results_path)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def copied_run(self, name):
        temporary = tempfile.TemporaryDirectory(dir=ROOT)
        run = Path(temporary.name) / name
        shutil.copytree(
            ROOT / "artifacts/evals/runs" / name,
            run,
            ignore=shutil.ignore_patterns(".next", ".vinext", ".wrangler", "coverage", "dist", "node_modules"),
        )
        results = json.loads((ROOT / "artifacts/evals/results.json").read_text(encoding="utf-8"))
        entry = next(case for case in results["cases"] if case["name"] == name)
        entry["result"] = str(run.relative_to(ROOT) / "result.json")
        results_path = Path(temporary.name) / "results.json"
        results_path.write_text(json.dumps(results), encoding="utf-8")
        return temporary, run, results_path

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
        result = self.run_checker(ROOT / "artifacts/evals/results.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("7 cases passed", result.stdout)

    def test_results_use_exact_kinds_and_run_record_references(self):
        results = json.loads((ROOT / "artifacts/evals/results.json").read_text(encoding="utf-8"))
        self.assertEqual({case["name"] for case in results["cases"]}, NAMES)
        for case in results["cases"]:
            with self.subTest(name=case["name"]):
                self.assertEqual(case["kind"], RUN_KINDS[case["name"]])
                if case["name"] in {"stale-approval", "self-approval"}:
                    self.assertNotIn("result", case)
                else:
                    self.assertTrue((ROOT / case["result"]).is_file())

    def test_adapter_contract_defines_capability_failure_and_snapshot_binding(self):
        contract = (ROOT / "adapters/adapter-contract.md").read_text(encoding="utf-8")
        for phrase in [
            "Capability predicates",
            "permitted fallback",
            '"status": "failed"',
            '"location": null',
            '"rendered_hash": null',
            "no issue-review",
            "current, issued, and rendered",
        ]:
            self.assertIn(phrase, contract)
        for name in ("claude", "opencode", "qwen-code"):
            text = (ROOT / f"adapters/{name}.md").read_text(encoding="utf-8")
            self.assertIn("capability", text.lower())
            self.assertIn("fallback", text.lower())

        self.assertIn('"rendered_hash": "<input snapshot sha256-v1 digest>"', contract)
        self.assertNotIn('"rendered_hash": "<issued sha256-v1 digest>"', contract)

    def test_checker_rejects_empty_or_gibberish_run_capture(self):
        for capture in ([], ["unrelated text"]):
            with self.subTest(capture=capture):
                temporary, run, results_path = self.copied_run("conflict")
                try:
                    record_path = run / "result.json"
                    record = json.loads(record_path.read_text(encoding="utf-8"))
                    record["captured_output"] = capture
                    record_path.write_text(json.dumps(record), encoding="utf-8")
                    self.assertNotEqual(self.run_checker(results_path).returncode, 0)
                finally:
                    temporary.cleanup()

    def test_checker_rejects_arbitrary_kind_and_missing_evidence(self):
        temporary, run, results_path = self.copied_run("existing-repo")
        try:
            results = json.loads(results_path.read_text(encoding="utf-8"))
            next(case for case in results["cases"] if case["name"] == "existing-repo")["kind"] = "anything"
            results_path.write_text(json.dumps(results), encoding="utf-8")
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)

            results = json.loads((ROOT / "artifacts/evals/results.json").read_text(encoding="utf-8"))
            next(case for case in results["cases"] if case["name"] == "existing-repo")["result"] = str(run.relative_to(ROOT) / "result.json")
            results_path.write_text(json.dumps(results), encoding="utf-8")
            record_path = run / "result.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["evidence_files"].append("missing.md")
            record_path.write_text(json.dumps(record), encoding="utf-8")
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()

    def test_checker_rejects_empty_evidence_list(self):
        temporary, run, results_path = self.copied_run("existing-repo")
        try:
            record_path = run / "result.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["evidence_files"] = []
            record_path.write_text(json.dumps(record), encoding="utf-8")
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()

    def test_checker_rejects_missing_site_or_digest_mismatch(self):
        for mutation in ("missing-site", "digest-mismatch"):
            with self.subTest(mutation=mutation):
                temporary, run, results_path = self.copied_run("critical-unknown")
                try:
                    record_path = run / "result.json"
                    record = json.loads(record_path.read_text(encoding="utf-8"))
                    if mutation == "missing-site":
                        record["site_reference"] = "alignment-review/missing.json"
                        record_path.write_text(json.dumps(record), encoding="utf-8")
                    else:
                        site_path = run / "alignment-review/site-review.json"
                        site = json.loads(site_path.read_text(encoding="utf-8"))
                        site["snapshot"]["digest"] = "0" * 64
                        site_path.write_text(json.dumps(site), encoding="utf-8")
                    self.assertNotEqual(self.run_checker(results_path).returncode, 0)
                finally:
                    temporary.cleanup()

    def test_checker_scans_forbidden_claims_in_record_site_transcript_and_evidence(self):
        for location in ("record", "site-reference", "transcript", "evidence"):
            with self.subTest(location=location):
                temporary, run, results_path = self.copied_run("critical-unknown")
                try:
                    record_path = run / "result.json"
                    record = json.loads(record_path.read_text(encoding="utf-8"))
                    phrase = "machine certification passed"
                    if location == "record":
                        record["captured_output"].append(phrase)
                    elif location == "site-reference":
                        record["site_reference"] += "#" + phrase
                    elif location == "transcript":
                        (run / "transcript.md").write_text(phrase, encoding="utf-8")
                    else:
                        (run / "alignment/review.md").write_text(phrase, encoding="utf-8")
                    record_path.write_text(json.dumps(record), encoding="utf-8")
                    self.assertNotEqual(self.run_checker(results_path).returncode, 0)
                finally:
                    temporary.cleanup()

    def test_checker_rejects_claimed_block_when_helper_gate_is_ready(self):
        temporary, run, results_path = self.copied_run("conflict")
        try:
            command = [
                str(ROOT / "scripts/alignment"), "issue-review", str(run),
                "--adapter", "eval-test", "--status", "presented", "--location", "site://eval",
            ]
            issued = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, check=True).stdout.strip().split(":", 1)[1]
            subprocess.run(
                [str(ROOT / "scripts/alignment"), "decide", str(run), "--decision", "approved", "--reviewer", "human", "--provenance", "human-message", "--review-hash", issued],
                cwd=ROOT,
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            )
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()

    def test_checker_rejects_forbidden_claim_in_unlisted_site_source(self):
        temporary, run, results_path = self.copied_run("greenfield")
        try:
            source = run / "alignment-review/site/app/page.tsx"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text("export default function Page() { return <>site approval button</>; }\n", encoding="utf-8")
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()

    def test_checker_rejects_omitted_snapshot_file_from_evidence(self):
        temporary, run, results_path = self.copied_run("existing-repo")
        try:
            record_path = run / "result.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["evidence_files"].remove("alignment/charter.md")
            record_path.write_text(json.dumps(record), encoding="utf-8")
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()

    def test_checker_rejects_keyword_gibberish_transcript(self):
        temporary, run, results_path = self.copied_run("critical-unknown")
        try:
            (run / "transcript.md").write_text(
                "review snapshot payload keys issue-review ready=false keyword gibberish\n",
                encoding="utf-8",
            )
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()

    def test_checker_rejects_formatted_nonsense_transcript(self):
        temporary, run, results_path = self.copied_run("critical-unknown")
        try:
            (run / "transcript.md").write_text(
                """# Critical-unknown eval transcript

## Request and initialization event

1. review snapshot payload keys issue-review check gate

## Action, output, review, snapshot, and gate event

1. review snapshot payload keys issue-review check gate
2. review snapshot payload keys issue-review check gate
3. review snapshot payload keys issue-review check gate
4. review snapshot payload keys issue-review check gate
5. review snapshot payload keys issue-review check gate
6. review snapshot payload keys issue-review check gate
""",
                encoding="utf-8",
            )
            result = self.run_checker(results_path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("event schema", result.stderr)
        finally:
            temporary.cleanup()

    def test_checker_rejects_duplicate_transcript_action_ids(self):
        temporary, run, results_path = self.copied_run("conflict")
        try:
            transcript = run / "transcript.md"
            text = transcript.read_text(encoding="utf-8")
            transcript.write_text(text.replace('"action_id":"A004"', '"action_id":"A001"'), encoding="utf-8")
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()

    def test_checker_rejects_init_argv_and_result_not_bound_to_manifest(self):
        for mutation in ("project-id", "result"):
            with self.subTest(mutation=mutation):
                temporary, run, results_path = self.copied_run("existing-repo")
                try:
                    transcript = run / "transcript.md"
                    text = transcript.read_text(encoding="utf-8")
                    if mutation == "project-id":
                        text = text.replace(
                            '"--project-id","existing-repo-export"',
                            '"--project-id","nonexistent-project"',
                        )
                    else:
                        text = text.replace(
                            '"output":{"alignment":"alignment"}',
                            '"output":{"alignment":"fabricated"}',
                        )
                    transcript.write_text(text, encoding="utf-8")
                    self.assertNotEqual(self.run_checker(results_path).returncode, 0)
                finally:
                    temporary.cleanup()

    def test_checker_rejects_impossible_argv_and_issue_location(self):
        for mutation in ("extra-snapshot-flag", "issue-location"):
            with self.subTest(mutation=mutation):
                temporary, run, results_path = self.copied_run("critical-unknown")
                try:
                    transcript = run / "transcript.md"
                    text = transcript.read_text(encoding="utf-8")
                    if mutation == "extra-snapshot-flag":
                        text = text.replace(
                            '"snapshot","<run-dir>","--json"]',
                            '"snapshot","<run-dir>","--json","--fabricated"]',
                        )
                    else:
                        text = text.replace(
                            '"--location","alignment-review/site-review.json"]',
                            '"--location","alignment-review/not-issued.json"]',
                        )
                    transcript.write_text(text, encoding="utf-8")
                    self.assertNotEqual(self.run_checker(results_path).returncode, 0)
                finally:
                    temporary.cleanup()

    def test_checker_rejects_manifest_renderer_location_contradiction(self):
        temporary, run, results_path = self.copied_run("existing-repo")
        try:
            manifest_path = run / "alignment/manifest.yaml"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["renderer"]["location"] = "alignment-review/not-issued.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()

    def test_checker_rejects_stale_digest_in_result_record(self):
        temporary, run, results_path = self.copied_run("conflict")
        try:
            record_path = run / "result.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["captured_output"].append("snapshot -> sha256-v1:" + "f" * 64)
            record_path.write_text(json.dumps(record), encoding="utf-8")
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()

    def test_checker_rejects_command_result_bound_to_wrong_evidence(self):
        temporary, run, results_path = self.copied_run("greenfield")
        try:
            transcript = run / "transcript.md"
            text = transcript.read_text(encoding="utf-8").replace(
                '"evidence":["alignment/review-state.json"],"action_id":"A003"',
                '"evidence":["alignment/manifest.yaml"],"action_id":"A003"',
            )
            transcript.write_text(text, encoding="utf-8")
            self.assertNotEqual(self.run_checker(results_path).returncode, 0)
        finally:
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
