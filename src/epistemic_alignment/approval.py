import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .models import GateResult, Snapshot
from .snapshot import create_snapshot


_STATE_NAME = "review-state.json"
_SCHEMA_VERSION = "1.0"
_PRESENTATION_STATUSES = {"draft", "presented", "published"}
_DECISIONS = {"approved", "changes_requested", "rejected"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _state_path(alignment_dir: Path) -> Path:
    return alignment_dir / _STATE_NAME


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


def _issued_hashes(state: Dict[str, Any]) -> Tuple[str, str]:
    issued = state["snapshot"].get("issued_hash")
    rendered = state["presentation"].get("rendered_hash")
    return _require_text(issued, "issued hash"), _require_text(rendered, "rendered hash")


def issue_review(alignment_dir: Path, adapter: str, status: str, location: str) -> Snapshot:
    if status not in _PRESENTATION_STATUSES:
        raise ValueError(f"unsupported presentation status: {status}")
    _require_text(adapter, "adapter")
    _require_text(location, "location")

    snapshot = create_snapshot(alignment_dir)
    state = _load_state(alignment_dir)
    timestamp = _utc_now()
    state["snapshot"].update(
        {
            "algorithm": snapshot.algorithm,
            "issued_hash": snapshot.digest,
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
            "rendered_at": timestamp,
        }
    )
    state["decision"] = {}
    state["handoff"] = {}
    _write_state(alignment_dir, state)
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

    current = create_snapshot(alignment_dir)
    state = _load_state(alignment_dir)
    issued, rendered = _issued_hashes(state)
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
    _write_state(alignment_dir, state)


def check_gate(alignment_dir: Path) -> GateResult:
    try:
        current = create_snapshot(alignment_dir)
    except ValueError:
        return GateResult(ready=False, reasons=["snapshot-invalid"], digest="")

    try:
        state = _load_state(alignment_dir)
    except ValueError:
        return GateResult(ready=False, reasons=["review-state-invalid"], digest=current.digest)

    reasons = []
    issued = state["snapshot"].get("issued_hash")
    rendered = state["presentation"].get("rendered_hash")
    decision = state["decision"]
    if not isinstance(issued, str) or not issued or not isinstance(rendered, str) or not rendered:
        reasons.append("review-not-issued")
    if state["presentation"].get("status") not in {"presented", "published"}:
        reasons.append("presentation-not-presented")
    if decision.get("decision") != "approved":
        reasons.append("decision-not-approved")
    if decision.get("provenance") != "human-message":
        reasons.append("non-human-provenance")
    if isinstance(issued, str) and issued and current.digest != issued:
        reasons.append("stale-approval")
    if not (
        issued == rendered == decision.get("review_hash") == current.digest
    ):
        reasons.append("hash-mismatch")
    return GateResult(ready=not reasons, reasons=reasons, digest=current.digest)
