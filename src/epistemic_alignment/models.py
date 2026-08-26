from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class Entity:
    id: str
    kind: str
    status: str
    priority: str
    source_kind: str
    source_ref: str
    confidence: str
    links: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class ArtifactSet:
    root: Path
    manifest: Dict[str, Any]
    entities: Dict[str, Entity]
    files: List[Path]
