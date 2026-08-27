from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class Dossier:
    root: Path
    manifest: Dict[str, Any]
    snapshot_paths: List[str]


@dataclass(frozen=True)
class Snapshot:
    algorithm: str
    digest: str
    paths: List[str]
