# pipeline_v2/core/storage/graph/graph_schema.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class NodeRecordV2:
    id: str
    type: str
    name: str
    canonical: str
    metadata: Dict[str, Any]


@dataclass
class EdgeRecordV2:
    id: str
    source: str
    target: str
    type: str
    layer: str
    status: str
    confidence: float
    metadata: Dict[str, Any]
