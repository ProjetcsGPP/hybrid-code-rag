# pipeline_v2/core/graph/graph_types.py

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class GraphNodeV2:
    id: str
    type: str  # symbol, function, class, variable
    name: str
    canonical: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdgeV2:
    id: str
    source: str
    target: str
    type: str  # BELONGS_TO, CALLS, IMPORTS, BINDS, EXTENDS
    layer: str  # STRUCTURAL | SEMANTIC | RUNTIME
    status: str  # RESOLVED | UNRESOLVED | APPROXIMATE
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
