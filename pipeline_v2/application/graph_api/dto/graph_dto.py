# pipeline_v2/application/graph_api/dto/graph_dto.py

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class NodeDTO:
    id: str
    type: str
    name: str
    canonical: str
    metadata: Dict[str, Any]


@dataclass
class EdgeDTO:
    id: str
    source: str
    target: str
    type: str
    layer: str
    status: str
    confidence: float
    metadata: Dict[str, Any]


@dataclass
class SubgraphDTO:
    nodes: List[NodeDTO]
    edges: List[EdgeDTO]


@dataclass
class TraceDTO:
    node: Optional[NodeDTO]
    from_edges: List[EdgeDTO]
    to_edges: List[EdgeDTO]
