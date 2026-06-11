# pipeline_v2/core/contract/graph_contracts.py


from dataclasses import dataclass, field
from typing import Dict, List, Optional

from pipeline_v2.core.graph.graph_types import GraphEdgeV2, GraphNodeV2


@dataclass(frozen=True)
class GraphSubgraphV2:
    nodes: List[GraphNodeV2] = field(default_factory=list)
    edges: List[GraphEdgeV2] = field(default_factory=list)

    def __contains__(self, key: str) -> bool:
        return key in {"nodes", "edges"}

    def __getitem__(self, key: str):
        if key == "nodes":
            return self.nodes
        if key == "edges":
            return self.edges
        raise KeyError(key)


@dataclass(frozen=True)
class GraphRetrievalResultV2:
    seed: str
    ranked_nodes: List[tuple[str, float]]
    subgraph: GraphSubgraphV2


@dataclass(frozen=True)
class GraphQueryContract:
    start: str
    depth: int = 1
    edge_type: Optional[str] = None
    layer: Optional[str] = None
    status: Optional[str] = None
    framework_hint: Optional[str] = None


@dataclass(frozen=True)
class GraphAnalysisInputV2:
    nodes: List[GraphNodeV2] = field(default_factory=list)
    edges: List[GraphEdgeV2] = field(default_factory=list)


@dataclass(frozen=True)
class RuntimeTraceEventV2:
    source: str
    target: str
    type: str
    state: str = "PROPAGATED"


@dataclass(frozen=True)
class ClassifiedRuntimeTraceEventV2:
    source: str
    target: str
    type: str
    state: str
    flow_type: str


@dataclass(frozen=True)
class RuntimeEdgeEventV2:
    edge_id: str
    source: str
    target: str
    state: str


@dataclass(frozen=True)
class RuntimeExecutionResultV2:
    states: Dict[str, str]
    trace: List[RuntimeTraceEventV2] = field(default_factory=list)
    runtime_edges: List[RuntimeEdgeEventV2] = field(default_factory=list)


@dataclass(frozen=True)
class RankingContextV2:
    seed: Optional[str] = None


@dataclass(frozen=True)
class ReasoningResultV2:
    risk_scores: Dict[str, float] = field(default_factory=dict)
    impact_analysis: Dict[str, List[str]] = field(default_factory=dict)
    critical_nodes: frozenset[str] = frozenset()
    reasoned_paths: List[List[str]] = field(default_factory=list)
    inferred_intent: str = "UNKNOWN"


@dataclass(frozen=True)
class RankedNodeV2:
    id: str
    name: str
    type: str
    score: float


@dataclass(frozen=True)
class AssignmentContractV2:
    variable: str
    source: str
    semantic_type: str = "unknown"
    model: Optional[str] = None
    confidence: float = 0.50
    framework_hint: Optional[str] = None


@dataclass(frozen=True)
class InheritanceEdgeV2:
    base_symbol_name: str
    resolved_base_symbol_id: Optional[str] = None
