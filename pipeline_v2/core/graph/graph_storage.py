# pipeline_v2/core/graph/graph_storage.py

from typing import Dict, List, Optional
from dataclasses import dataclass, field
import uuid


@dataclass
class GraphNode:
    id: str
    type: str
    payload: dict


@dataclass
class GraphEdge:
    id: str
    source: str
    target: str
    type: str
    metadata: dict = field(default_factory=dict)


class GraphStorageV2:
    """
    Storage layer do grafo semântico V2.

    Não é apenas persistência:
    é estrutura navegável de relação semântica.
    """

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}

        self.out_index: Dict[str, List[str]] = {}
        self.in_index: Dict[str, List[str]] = {}

    # --------------------
    # NODE OPS (SYMBOL CORE)
    # --------------------

    def add_node(self, node_type: str, payload: dict) -> str:
        node_id = str(uuid.uuid4())

        node = GraphNode(id=node_id, type=node_type, payload=payload)

        self.nodes[node_id] = node
        self.out_index[node_id] = []
        self.in_index[node_id] = []

        return node_id

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self.nodes.get(node_id)

    # --------------------
    # EDGE OPS (RELATIONSHIP CORE)
    # --------------------

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: str,
        metadata: Optional[dict] = None,
    ) -> str:

        edge_id = str(uuid.uuid4())

        edge = GraphEdge(
            id=edge_id,
            source=source_id,
            target=target_id,
            type=edge_type,
            metadata=metadata or {},
        )

        self.edges[edge_id] = edge

        self.out_index.setdefault(source_id, []).append(edge_id)
        self.in_index.setdefault(target_id, []).append(edge_id)

        return edge_id

    # --------------------
    # GRAPH NAVIGATION (ESSENCIAL PARA RAG V2)
    # --------------------

    def get_outgoing(self, node_id: str) -> List[GraphEdge]:
        return [self.edges[eid] for eid in self.out_index.get(node_id, [])]

    def get_incoming(self, node_id: str) -> List[GraphEdge]:
        return [self.edges[eid] for eid in self.in_index.get(node_id, [])]

    def neighbors(self, node_id: str) -> List[GraphNode]:
        edges = self.get_outgoing(node_id)
        return [self.nodes[e.target] for e in edges if e.target in self.nodes]

    # --------------------
    # DEBUG / INTROSPECTION
    # --------------------

    def summary(self) -> dict:
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "density": len(self.edges) / max(len(self.nodes), 1),
        }
