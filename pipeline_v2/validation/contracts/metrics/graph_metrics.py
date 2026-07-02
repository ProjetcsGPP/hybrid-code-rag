# pipeline_v2/validation/contracts/metrics/graph_metrics.py

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class GraphMetrics:

    total_nodes: int

    total_edges: int

    node_types: Dict[str, int] = field(default_factory=dict)

    edge_types: Dict[str, int] = field(default_factory=dict)
