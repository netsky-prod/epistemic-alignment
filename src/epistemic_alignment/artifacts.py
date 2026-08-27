import json
import shutil
from pathlib import Path
from typing import Any, Dict

from .models import Dossier


TEMPLATE_ROOT = Path(__file__).resolve().parents[2] / "templates" / "alignment"


def _write_text(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(content.replace("\r\n", "\n").replace("\r", "\n"))


def initialize(target_root: Path, project_id: str, title: str) -> Path:
    alignment_dir = target_root / "alignment"
    if alignment_dir.exists():
        raise FileExistsError(f"alignment directory already exists: {alignment_dir}")

    target_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE_ROOT, alignment_dir)
    for path in alignment_dir.rglob("*"):
        if path.is_file():
            content = path.read_text(encoding="utf-8")
            if path.name == "manifest.yaml":
                manifest = json.loads(content)
                manifest["project"] = {"id": project_id, "title": title}
                content = json.dumps(manifest, indent=2) + "\n"
            _write_text(
                path,
                content,
            )
    return alignment_dir


def load_dossier(alignment_dir: Path) -> Dossier:
    manifest = json.loads((alignment_dir / "manifest.yaml").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "1.0":
        raise ValueError("unsupported manifest schema version")

    snapshot_paths = manifest.get("snapshot_paths")
    if not isinstance(snapshot_paths, list) or not all(
        isinstance(path, str) for path in snapshot_paths
    ):
        raise ValueError("manifest snapshot_paths must be a list of strings")

    return Dossier(
        root=alignment_dir,
        manifest=manifest,
        snapshot_paths=snapshot_paths,
    )
