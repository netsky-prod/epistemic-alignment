import copy
import hashlib
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .approval import (
    _handoff_backup_path,
    _handoff_pending_path,
    _load_state,
    _read_regular_handoff,
    _remove_handoff,
    _restore_handoff,
    _write_state,
    check_gate,
    mutation_lock,
)
from .artifacts import load_dossier
from .snapshot import create_snapshot


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


def _begin_handoff_transaction(alignment_dir: Path):
    handoff_path = alignment_dir / "handoff.md"
    backup_path = _handoff_backup_path(alignment_dir)
    pending_path = _handoff_pending_path(alignment_dir)
    if os.path.lexists(str(backup_path)) or os.path.lexists(str(pending_path)):
        raise ValueError("unresolved handoff transaction blocks handoff generation")

    descriptor = None
    try:
        descriptor = os.open(
            str(pending_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600
        )
        os.fsync(descriptor)
    except BaseException:
        if descriptor is not None:
            os.close(descriptor)
        try:
            pending_path.unlink()
        except FileNotFoundError:
            pass
        raise
    else:
        os.close(descriptor)

    had_previous = os.path.lexists(str(handoff_path))
    try:
        if had_previous:
            os.replace(handoff_path, backup_path)
    except BaseException:
        pending_path.unlink()
        raise
    return pending_path, backup_path, had_previous


def _rollback_handoff_transaction(
    alignment_dir: Path,
    pending_path: Path,
    backup_path: Path,
    had_previous: bool,
    previous_state,
) -> None:
    handoff_path = alignment_dir / "handoff.md"
    _remove_handoff(alignment_dir)
    if _load_state(alignment_dir) != previous_state:
        _write_state(alignment_dir, previous_state)
    if had_previous:
        _restore_handoff(backup_path, handoff_path)
    pending_path.unlink()


def _commit_handoff_transaction(
    pending_path: Path, backup_path: Path, had_previous: bool
) -> None:
    if had_previous:
        backup_path.unlink()
    pending_path.unlink()


def write_handoff(alignment_dir: Path) -> Path:
    with mutation_lock(alignment_dir):
        initial_gate = check_gate(alignment_dir)
        if not initial_gate.ready:
            raise ValueError("handoff gate is not ready: " + ", ".join(initial_gate.reasons))
        expected_digest = initial_gate.digest

        dossier = load_dossier(alignment_dir)
        previous_state = _load_state(alignment_dir)
        findings = previous_state["decision"]["acknowledged_findings"]
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
        if _load_state(alignment_dir) != previous_state:
            _clear_failed_handoff(alignment_dir)
            raise ValueError("handoff state changed before writing")

        content_sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
        pending_path, backup_path, had_previous = _begin_handoff_transaction(alignment_dir)
        try:
            _write_text_atomically(handoff_path, content)
            current = create_snapshot(alignment_dir)
            if current.digest != expected_digest or _load_state(alignment_dir) != previous_state:
                raise ValueError("handoff gate became stale while writing")
            if hashlib.sha256(_read_regular_handoff(handoff_path)).hexdigest() != content_sha256:
                raise ValueError("handoff bytes changed while writing")

            state = copy.deepcopy(previous_state)
            state["handoff"] = {
                "algorithm": "sha256-v1",
                "content_sha256": content_sha256,
                "digest": expected_digest,
                "verified_at": _utc_now(),
            }
            _write_state(alignment_dir, state)
            current = create_snapshot(alignment_dir)
            if current.digest != expected_digest:
                raise ValueError("handoff gate became stale while recording")
            if hashlib.sha256(_read_regular_handoff(handoff_path)).hexdigest() != content_sha256:
                raise ValueError("handoff bytes changed while recording")
        except BaseException:
            _rollback_handoff_transaction(
                alignment_dir,
                pending_path,
                backup_path,
                had_previous,
                previous_state,
            )
            raise
        _commit_handoff_transaction(pending_path, backup_path, had_previous)

        after_state_write = check_gate(alignment_dir)
        if not after_state_write.ready or after_state_write.digest != expected_digest:
            _clear_failed_handoff(alignment_dir)
            raise ValueError("handoff gate became stale while recording")
        return handoff_path
