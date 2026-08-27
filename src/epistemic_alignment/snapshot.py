import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import List

from .artifacts import load_dossier
from .models import Snapshot


def _safe_paths(alignment_dir: Path, declared_paths: List[str]) -> List[str]:
    root = alignment_dir.resolve()
    resolved_paths = []
    seen = set()
    for path in declared_paths:
        if not _is_relative_posix_path(path):
            raise ValueError(f"unsafe snapshot path: {path!r}")
        if path in seen:
            raise ValueError(f"duplicate snapshot path: {path}")
        seen.add(path)

        target = (root / PurePosixPath(path)).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            raise ValueError(f"snapshot path escapes dossier: {path}") from None
        if not target.is_file():
            raise ValueError(f"snapshot path is missing or not a file: {path}")
        resolved_paths.append(path)
    return sorted(resolved_paths)


def _is_relative_posix_path(path: str) -> bool:
    if not path or "\\" in path:
        return False
    candidate = PurePosixPath(path)
    if candidate.is_absolute():
        return False
    return all(segment not in ("", ".", "..") for segment in path.split("/"))


def _normalized_text(path: Path) -> bytes:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"snapshot path is not valid UTF-8: {path}") from error
    return content.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _update_length_prefixed(digest, value: bytes) -> None:
    digest.update(len(value).to_bytes(8, byteorder="big"))
    digest.update(value)


def create_snapshot(alignment_dir: Path) -> Snapshot:
    dossier = load_dossier(alignment_dir)
    paths = _safe_paths(dossier.root, dossier.snapshot_paths)
    header = {
        "schema_version": dossier.manifest["schema_version"],
        "project": dossier.manifest.get("project"),
        "snapshot_paths": paths,
    }
    digest = hashlib.sha256()
    _update_length_prefixed(
        digest,
        json.dumps(header, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"),
    )
    root = dossier.root.resolve()
    for path in paths:
        _update_length_prefixed(digest, path.encode("utf-8"))
        _update_length_prefixed(
            digest, _normalized_text((root / PurePosixPath(path)).resolve())
        )
    return Snapshot(algorithm="sha256-v1", digest=digest.hexdigest(), paths=paths)
