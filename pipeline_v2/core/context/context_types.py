# pipeline_v2/core/context/context_types.py

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ContextNode:
    id: str
    type: str
    name: str
    canonical: str
    metadata: Dict[str, Any]


@dataclass
class ContextEdge:
    id: str
    source: str
    target: str
    type: str
    layer: str
    status: str
    confidence: float
    metadata: Dict[str, Any]


@dataclass
class GraphContext:
    focus_node: ContextNode
    nodes: List[ContextNode]
    edges: List[ContextEdge]

    semantic_trace: Dict[str, Any]
    ranked_score: Dict[str, float]

    metadata: Dict[str, Any]
