import hashlib
import json
import os
import stat
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List

from .models import GateResult, Snapshot
from .snapshot import create_snapshot


_STATE_NAME = "review-state.json"
_SCHEMA_VERSION = "1.0"
_PRESENTATION_STATUSES = {"draft", "presented", "published"}
_DECISIONS = {"approved", "changes_requested", "rejected"}
_SNAPSHOT_ALGORITHM = "sha256-v1"
_LOCK_NAME = ".alignment-gate.lock"
_HANDOFF_PENDING_NAME = ".handoff-pending"
_LOCK_TIMEOUT_SECONDS = 5


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _state_path(alignment_dir: Path) -> Path:
    return alignment_dir / _STATE_NAME


def _handoff_path(alignment_dir: Path) -> Path:
    return alignment_dir / "handoff.md"


def _handoff_backup_path(alignment_dir: Path) -> Path:
    return alignment_dir / ".handoff-backup"


def _handoff_pending_path(alignment_dir: Path) -> Path:
    return alignment_dir / _HANDOFF_PENDING_NAME


@contextmanager
def mutation_lock(alignment_dir: Path) -> Iterator[None]:
    lock_path = alignment_dir / _LOCK_NAME
    deadline = time.monotonic() + _LOCK_TIMEOUT_SECONDS
    while True:
        try:
            os.mkdir(lock_path)
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise ValueError("timed out waiting for the dossier mutation lock") from None
            time.sleep(0.01)
    try:
        yield
    finally:
        os.rmdir(lock_path)


def _load_state(alignment_dir: Path) -> Dict[str, Any]:
    path = _state_path(alignment_dir)
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"review state is missing: {path}") from None
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(f"review state is invalid: {path}") from error
    if not isinstance(state, dict) or state.get("schema_version") != _SCHEMA_VERSION:
        raise ValueError("unsupported review state schema version")
    for section in ("snapshot", "presentation", "decision", "handoff"):
        if section not in state:
            state[section] = {}
        if not isinstance(state[section], dict):
            raise ValueError(f"review state {section} must be an object")
    return state


def _write_state(alignment_dir: Path, state: Dict[str, Any]) -> None:
    path = _state_path(alignment_dir)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=".review-state-", suffix=".tmp"
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(state, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _require_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _require_string_list(value: Any, name: str) -> List[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{name} must be a list of strings")
    return value


def _require_sha256(value: Any, name: str) -> str:
    value = _require_text(value, name)
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")
    return value


def _validate_issuance_state(state: Dict[str, Any]) -> None:
    snapshot = state["snapshot"]
    presentation = state["presentation"]
    if snapshot.get("algorithm") != _SNAPSHOT_ALGORITHM:
        raise ValueError("unsupported snapshot algorithm in review state")
    _require_sha256(snapshot.get("digest"), "snapshot digest")
    _require_string_list(snapshot.get("paths"), "snapshot paths")
    _require_text(snapshot.get("issued_at"), "snapshot issued_at")
    _require_text(presentation.get("adapter"), "presentation adapter")
    if presentation.get("status") not in _PRESENTATION_STATUSES:
        raise ValueError("unsupported presentation status in review state")
    _require_text(presentation.get("location"), "presentation location")
    _require_sha256(presentation.get("rendered_hash"), "presentation rendered hash")
    _require_text(presentation.get("presented_at"), "presentation presented_at")


def _validate_complete_state(state: Dict[str, Any]) -> None:
    _validate_issuance_state(state)
    decision = state["decision"]
    if decision.get("decision") not in _DECISIONS:
        raise ValueError("unsupported decision in review state")
    _require_text(decision.get("reviewer"), "decision reviewer")
    _require_text(decision.get("provenance"), "decision provenance")
    _require_text(decision.get("decided_at"), "decision decided_at")
    _require_sha256(decision.get("review_hash"), "decision review hash")
    _require_string_list(decision.get("acknowledged_findings"), "acknowledged findings")
    handoff = state["handoff"]
    if handoff:
        if handoff.get("algorithm") != _SNAPSHOT_ALGORITHM:
            raise ValueError("unsupported handoff algorithm in review state")
        _require_sha256(handoff.get("digest"), "handoff digest")
        _require_sha256(handoff.get("content_sha256"), "handoff content SHA-256")
        _require_text(handoff.get("verified_at"), "handoff verified_at")


def _read_regular_handoff(path: Path) -> bytes:
    try:
        path_before = path.lstat()
    except OSError as error:
        raise ValueError("handoff file is unavailable") from error
    if not stat.S_ISREG(path_before.st_mode):
        raise ValueError("handoff path must be a regular non-symlink file")

    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = None
    try:
        descriptor = os.open(str(path), flags)
        opened_before = os.fstat(descriptor)
        if not stat.S_ISREG(opened_before.st_mode) or (
            opened_before.st_dev,
            opened_before.st_ino,
        ) != (path_before.st_dev, path_before.st_ino):
            raise ValueError("handoff path changed while opening")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None
            content = stream.read()
            opened_after = os.fstat(stream.fileno())
        if (
            opened_after.st_dev,
            opened_after.st_ino,
            opened_after.st_size,
            opened_after.st_mtime_ns,
            opened_after.st_ctime_ns,
        ) != (
            opened_before.st_dev,
            opened_before.st_ino,
            opened_before.st_size,
            opened_before.st_mtime_ns,
            opened_before.st_ctime_ns,
        ):
            raise ValueError("handoff file changed while reading")
        path_after = path.lstat()
        if not stat.S_ISREG(path_after.st_mode) or (
            path_after.st_dev,
            path_after.st_ino,
        ) != (opened_after.st_dev, opened_after.st_ino):
            raise ValueError("handoff path changed while reading")
        return content
    except OSError as error:
        raise ValueError("handoff file is unavailable") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _review_is_snapshotted(snapshot: Snapshot) -> bool:
    return "review.md" in snapshot.paths


def _remove_handoff(alignment_dir: Path) -> None:
    try:
        _handoff_path(alignment_dir).unlink()
    except FileNotFoundError:
        pass


def _move_handoff_to_backup(alignment_dir: Path) -> Path:
    handoff_path = _handoff_path(alignment_dir)
    backup_path = _handoff_backup_path(alignment_dir)
    if os.path.lexists(str(_handoff_pending_path(alignment_dir))):
        raise ValueError("unresolved handoff transaction blocks state mutation")
    if os.path.lexists(str(backup_path)):
        raise ValueError("unresolved handoff backup blocks state mutation")
    if not os.path.lexists(str(handoff_path)):
        return backup_path
    os.replace(handoff_path, backup_path)
    return backup_path


def _commit_handoff_invalidation(backup_path: Path) -> None:
    try:
        backup_path.unlink()
    except FileNotFoundError:
        pass


def _restore_handoff(backup_path: Path, handoff_path: Path) -> None:
    if os.path.lexists(str(backup_path)):
        os.replace(backup_path, handoff_path)


def _write_state_while_invalidating_handoff(
    alignment_dir: Path, state: Dict[str, Any]
) -> None:
    backup_path = _move_handoff_to_backup(alignment_dir)
    handoff_path = _handoff_path(alignment_dir)
    try:
        _write_state(alignment_dir, state)
    except BaseException:
        _restore_handoff(backup_path, handoff_path)
        raise
    _commit_handoff_invalidation(backup_path)


def issue_review(alignment_dir: Path, adapter: str, status: str, location: str) -> Snapshot:
    if status not in _PRESENTATION_STATUSES:
        raise ValueError(f"unsupported presentation status: {status}")
    _require_text(adapter, "adapter")
    _require_text(location, "location")

    with mutation_lock(alignment_dir):
        snapshot = create_snapshot(alignment_dir)
        if not _review_is_snapshotted(snapshot):
            raise ValueError("review.md must be included in snapshot paths")
        state = _load_state(alignment_dir)
        timestamp = _utc_now()
        state["snapshot"].update(
            {
                "algorithm": snapshot.algorithm,
                "digest": snapshot.digest,
                "paths": snapshot.paths,
                "issued_at": timestamp,
            }
        )
        state["presentation"].update(
            {
                "adapter": adapter,
                "status": status,
                "location": location,
                "rendered_hash": snapshot.digest,
                "presented_at": timestamp,
            }
        )
        state["decision"] = {}
        state["handoff"] = {}
        _write_state_while_invalidating_handoff(alignment_dir, state)
        return snapshot


def record_decision(
    alignment_dir: Path,
    decision: str,
    reviewer: str,
    provenance: str,
    review_hash: str,
    acknowledged_findings: List[str],
) -> None:
    if decision not in _DECISIONS:
        raise ValueError(f"unsupported decision: {decision}")
    _require_text(reviewer, "reviewer")
    _require_text(provenance, "provenance")
    _require_text(review_hash, "review hash")
    if not isinstance(acknowledged_findings, list) or not all(
        isinstance(finding, str) for finding in acknowledged_findings
    ):
        raise ValueError("acknowledged findings must be a list of strings")

    with mutation_lock(alignment_dir):
        current = create_snapshot(alignment_dir)
        if not _review_is_snapshotted(current):
            raise ValueError("review.md must be included in snapshot paths")
        state = _load_state(alignment_dir)
        _validate_issuance_state(state)
        issued = state["snapshot"]["digest"]
        rendered = state["presentation"]["rendered_hash"]
        if decision == "approved":
            if provenance != "human-message":
                raise ValueError("approved decisions require human-message provenance")
            if state["presentation"].get("status") not in {"presented", "published"}:
                raise ValueError("approved decisions require a presented or published review")
            if {review_hash, issued, rendered, current.digest} != {current.digest}:
                raise ValueError("approved decision hash must match issued, rendered, and current snapshot")

        state["decision"] = {
            "decision": decision,
            "reviewer": reviewer,
            "provenance": provenance,
            "review_hash": review_hash,
            "acknowledged_findings": acknowledged_findings,
            "decided_at": _utc_now(),
        }
        state["handoff"] = {}
        _write_state_while_invalidating_handoff(alignment_dir, state)


def check_gate(alignment_dir: Path) -> GateResult:
    try:
        current = create_snapshot(alignment_dir)
    except ValueError:
        return GateResult(ready=False, reasons=["snapshot-invalid"], digest="")

    if os.path.lexists(str(_handoff_backup_path(alignment_dir))) or os.path.lexists(
        str(_handoff_pending_path(alignment_dir))
    ):
        return GateResult(
            ready=False,
            reasons=["handoff-transaction-unresolved"],
            digest=current.digest,
        )

    if not _review_is_snapshotted(current):
        return GateResult(ready=False, reasons=["review-not-snapshotted"], digest=current.digest)

    try:
        state = _load_state(alignment_dir)
        _validate_complete_state(state)
    except ValueError:
        return GateResult(ready=False, reasons=["review-state-invalid"], digest=current.digest)

    reasons = []
    issued = state["snapshot"]["digest"]
    rendered = state["presentation"]["rendered_hash"]
    decision = state["decision"]
    if state["presentation"].get("status") not in {"presented", "published"}:
        reasons.append("presentation-not-presented")
    if decision.get("decision") != "approved":
        reasons.append("decision-not-approved")
    if decision.get("provenance") != "human-message":
        reasons.append("non-human-provenance")
    if current.digest != issued:
        reasons.append("stale-approval")
    if not (
        issued == rendered == decision.get("review_hash") == current.digest
    ):
        reasons.append("hash-mismatch")
    handoff = state["handoff"]
    handoff_path = _handoff_path(alignment_dir)
    handoff_exists = os.path.lexists(str(handoff_path))
    if handoff_exists and not handoff:
        reasons.append("handoff-state-missing")
    elif handoff:
        if not handoff_exists:
            reasons.append("handoff-file-missing")
        else:
            try:
                content = _read_regular_handoff(handoff_path)
            except ValueError:
                reasons.append("handoff-file-invalid")
            else:
                if (
                    handoff["digest"] != current.digest
                    or hashlib.sha256(content).hexdigest() != handoff["content_sha256"]
                ):
                    reasons.append("handoff-digest-mismatch")
    return GateResult(ready=not reasons, reasons=reasons, digest=current.digest)
