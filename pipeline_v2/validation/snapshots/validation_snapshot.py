# pipeline_v2/validation/snapshots/validation_snapshot.py

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass(frozen=True)
class ValidationSnapshot:

    # GRAPH
    nodes: Dict[str, Dict[str, Any]]
    edges: List[Dict[str, Any]]

    # IDENTITY
    registry: Dict[str, Dict[str, Any]]

    # INPUTS
    chunks: List[Dict[str, Any]]
    symbols: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]

    # META
    project_root: str
    snapshot_version: str = "v2"
