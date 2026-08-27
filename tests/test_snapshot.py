import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from epistemic_alignment.snapshot import create_snapshot


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/alignment"


class SnapshotTests(unittest.TestCase):
    def copy_dossier(self, directory):
        target = Path(directory) / "alignment"
        shutil.copytree(TEMPLATE, target)
        return target

    def replace_snapshot_paths(self, target, paths):
        manifest = json.loads((target / "manifest.yaml").read_text(encoding="utf-8"))
        manifest["snapshot_paths"] = paths
        (target / "manifest.yaml").write_text(json.dumps(manifest), encoding="utf-8")

    def test_hash_is_stable_across_manifest_path_order_and_crlf(self):
        with tempfile.TemporaryDirectory() as directory:
            left = self.copy_dossier(Path(directory) / "left")
            right = self.copy_dossier(Path(directory) / "right")
            manifest = json.loads((right / "manifest.yaml").read_text(encoding="utf-8"))
            manifest["snapshot_paths"].reverse()
            (right / "manifest.yaml").write_text(json.dumps(manifest), encoding="utf-8")
            charter = (right / "charter.md").read_text(encoding="utf-8")
            (right / "charter.md").write_bytes(charter.replace("\n", "\r\n").encode("utf-8"))
            self.assertEqual(create_snapshot(left).digest, create_snapshot(right).digest)

    def test_included_file_change_changes_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.copy_dossier(directory)
            before = create_snapshot(target).digest
            (target / "charter.md").write_text(
                (target / "charter.md").read_text(encoding="utf-8") + "\nChanged\n",
                encoding="utf-8",
            )
            self.assertNotEqual(before, create_snapshot(target).digest)

    def test_content_cannot_imitate_path_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            left = self.copy_dossier(Path(directory) / "left")
            right = self.copy_dossier(Path(directory) / "right")
            for target, first, second in (
                (left, "X", "Y\0b\0Z"),
                (right, "X\0b\0Y", "Z"),
            ):
                self.replace_snapshot_paths(target, ["a", "b"])
                (target / "a").write_text(first, encoding="utf-8")
                (target / "b").write_text(second, encoding="utf-8")
            self.assertNotEqual(create_snapshot(left).digest, create_snapshot(right).digest)

    def test_unsafe_duplicate_missing_and_non_file_paths_fail_closed(self):
        invalid_paths = [
            ["../secret"],
            ["/tmp/secret"],
            ["charter.md", "charter.md"],
            ["missing.md"],
            ["architecture"],
            ["./charter.md"],
            ["charter.md/"],
            ["architecture\\context.md"],
        ]
        for bad_paths in invalid_paths:
            with self.subTest(paths=bad_paths), tempfile.TemporaryDirectory() as directory:
                target = self.copy_dossier(directory)
                self.replace_snapshot_paths(target, bad_paths)
                with self.assertRaises(ValueError):
                    create_snapshot(target)

    def test_symlinks_resolving_outside_dossier_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.copy_dossier(directory)
            outside = Path(directory) / "outside.md"
            outside.write_text("outside", encoding="utf-8")
            link = target / "linked.md"
            try:
                os.symlink(outside, link)
            except (NotImplementedError, OSError) as error:
                self.skipTest(f"symlinks unavailable: {error}")
            self.replace_snapshot_paths(target, ["linked.md"])
            with self.assertRaises(ValueError):
                create_snapshot(target)

    def test_cli_emits_json_snapshot(self):
        result = subprocess.run(
            [str(ROOT / "scripts/alignment"), "snapshot", "templates", "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        snapshot = json.loads(result.stdout)
        self.assertEqual(snapshot["algorithm"], "sha256-v1")
        self.assertEqual(len(snapshot["digest"]), 64)
        self.assertEqual(snapshot["paths"], sorted(snapshot["paths"]))
