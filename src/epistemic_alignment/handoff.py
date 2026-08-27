import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .approval import _load_state, _write_state, check_gate
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


def write_handoff(alignment_dir: Path) -> Path:
    gate = check_gate(alignment_dir)
    if not gate.ready:
        raise ValueError("handoff gate is not ready: " + ", ".join(gate.reasons))

    dossier = load_dossier(alignment_dir)
    findings = _load_state(alignment_dir)["decision"].get("acknowledged_findings", [])
    project = dossier.manifest.get("project", {})
    title = project.get("title", project.get("id", "Alignment dossier"))
    handoff_path = alignment_dir / "handoff.md"
    content = "\n".join(
        [
            "# Alignment handoff: " + str(title),
            "",
            "Approved snapshot: sha256-v1:" + gate.digest,
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

    # A second fresh check closes the normal local-file TOCTOU window before
    # any generated artifact is published as a handoff.
    gate = check_gate(alignment_dir)
    if not gate.ready:
        raise ValueError("handoff gate is not ready: " + ", ".join(gate.reasons))
    _write_text_atomically(handoff_path, content)

    # Do not record a successful handoff if the snapshot changed while writing.
    gate = check_gate(alignment_dir)
    if not gate.ready:
        raise ValueError("handoff gate became stale: " + ", ".join(gate.reasons))
    state = _load_state(alignment_dir)
    state["handoff"].update(
        {
            "algorithm": "sha256-v1",
            "verified_hash": gate.digest,
            "verified_at": _utc_now(),
        }
    )
    _write_state(alignment_dir, state)
    return handoff_path
