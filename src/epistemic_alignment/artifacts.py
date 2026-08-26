import json
import shutil
from pathlib import Path
from typing import Any, Dict

from .models import ArtifactSet, Entity


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


def _front_matter(path: Path) -> Dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return {}
    _, metadata, _ = content.split("---\n", 2)
    return json.loads(metadata)


def load_artifact_set(alignment_dir: Path) -> ArtifactSet:
    manifest = json.loads((alignment_dir / "manifest.yaml").read_text(encoding="utf-8"))
    entities = {}
    for path in alignment_dir.rglob("*.md"):
        for entity_data in _front_matter(path).get("entities", []):
            entity = Entity(**entity_data)
            entities[entity.id] = entity
    return ArtifactSet(
        root=alignment_dir,
        manifest=manifest,
        entities=entities,
        files=sorted(path for path in alignment_dir.rglob("*") if path.is_file()),
    )
