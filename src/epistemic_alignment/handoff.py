import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .approval import (
    _load_state,
    _remove_handoff,
    _write_state,
    check_gate,
    mutation_lock,
)
from .artifacts import load_dossier


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_text_atomically(path: Path, content: str) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=".handoff-", suffix=".tmp"
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _clear_failed_handoff(alignment_dir: Path) -> None:
    _remove_handoff(alignment_dir)
    try:
        state = _load_state(alignment_dir)
    except ValueError:
        return
    state["handoff"] = {}
    _write_state(alignment_dir, state)


def write_handoff(alignment_dir: Path) -> Path:
    with mutation_lock(alignment_dir):
        initial_gate = check_gate(alignment_dir)
        if not initial_gate.ready:
            raise ValueError("handoff gate is not ready: " + ", ".join(initial_gate.reasons))
        expected_digest = initial_gate.digest

        dossier = load_dossier(alignment_dir)
        findings = _load_state(alignment_dir)["decision"]["acknowledged_findings"]
        project = dossier.manifest.get("project", {})
        title = project.get("title", project.get("id", "Alignment dossier"))
        handoff_path = alignment_dir / "handoff.md"
        content = "\n".join(
            [
                "# Alignment handoff: " + str(title),
                "",
                "Approved snapshot: sha256-v1:" + expected_digest,
                "",
                "Included dossier paths:",
                *["- " + path for path in dossier.snapshot_paths],
                "",
                "Semantic review: review.md",
                "",
                "Acknowledged findings:",
                *(["- " + finding for finding in findings] or ["- None recorded"]),
                "",
                "Next step: invoke superpowers:brainstorming with this dossier as required context before implementation.",
                "",
            ]
        )

        before_write = check_gate(alignment_dir)
        if not before_write.ready or before_write.digest != expected_digest:
            _clear_failed_handoff(alignment_dir)
            raise ValueError("handoff gate changed before writing")
        _write_text_atomically(handoff_path, content)

        after_write = check_gate(alignment_dir)
        if not after_write.ready or after_write.digest != expected_digest:
            _clear_failed_handoff(alignment_dir)
            raise ValueError("handoff gate became stale while writing")
        state = _load_state(alignment_dir)
        state["handoff"] = {
            "algorithm": "sha256-v1",
            "digest": expected_digest,
            "verified_at": _utc_now(),
        }
        _write_state(alignment_dir, state)
        after_state_write = check_gate(alignment_dir)
        if not after_state_write.ready or after_state_write.digest != expected_digest:
            _clear_failed_handoff(alignment_dir)
            raise ValueError("handoff gate became stale while recording")
        return handoff_path
