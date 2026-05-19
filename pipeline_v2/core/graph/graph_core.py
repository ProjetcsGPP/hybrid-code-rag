# pipeline_v2/core/graph/graph_core.py

from collections import defaultdict
from typing import Dict, List, Optional

from .graph_store import GraphStoreV2
from .graph_index import GraphIndexV2
from .graph_types import GraphNodeV2, GraphEdgeV2


class GraphCoreV2:
    """
    Graph Core V2:
    - store: persistência estrutural
    - index: aceleração de lookup
    - semantic views: leitura por camada/relacionamento
    """

    def __init__(self):
        self.store = GraphStoreV2()
        self.index = GraphIndexV2()

        # NOVO: índices de arestas por performance semântica
        self.edges_by_source: Dict[str, List[GraphEdgeV2]] = defaultdict(list)
        self.edges_by_target: Dict[str, List[GraphEdgeV2]] = defaultdict(list)
        self.edges_by_type: Dict[str, List[GraphEdgeV2]] = defaultdict(list)

    # -------------------------
    # NODES
    # -------------------------
    def add_node(self, node: GraphNodeV2):
        self.store.add_node(node)
        self.index.index_node(node)

    def get_node(self, node_id: str) -> Optional[GraphNodeV2]:
        return self.store.get_node(node_id)

    # -------------------------
    # EDGES (EVOLUÍDO)
    # -------------------------
    def add_edge(self, edge: GraphEdgeV2):
        """
        Agora edges são indexadas semanticamente também.
        """

        self.store.add_edge(edge)

        self.edges_by_source[edge.source].append(edge)
        self.edges_by_target[edge.target].append(edge)
        self.edges_by_type[edge.type].append(edge)

    # -------------------------
    # TRACE (ENRIQUECIDO)
    # -------------------------
    def trace(self, node_id: str):
        """
        Trace estrutural bidirecional.
        """

        return {
            "from": self.edges_by_source.get(node_id, []),
            "to": self.edges_by_target.get(node_id, []),
        }

    # -------------------------
    # NOVO: TRACE SEMÂNTICO
    # -------------------------
    def semantic_trace(
        self,
        node_id: str,
        layer: Optional[str] = None,
        status: Optional[str] = None,
    ):
        """
        Trace filtrado por camada semântica.
        """

        edges = self.edges_by_source.get(node_id, [])

        if layer:
            edges = [e for e in edges if getattr(e, "layer", None) == layer]

        if status:
            edges = [e for e in edges if getattr(e, "status", None) == status]

        return edges

    # -------------------------
    # NOVO: SUBGRAFO LOCAL
    # -------------------------
    def subgraph(self, node_id: str, depth: int = 1):
        """
        Extrai subgrafo local para contexto RAG.
        """

        visited = set()
        frontier = [node_id]

        nodes = {}
        edges = []

        for _ in range(depth):
            next_frontier = []

            for nid in frontier:
                if nid in visited:
                    continue
                visited.add(nid)

                node = self.store.get_node(nid)
                if node:
                    nodes[node.id] = node

                for e in self.edges_by_source.get(nid, []):
                    edges.append(e)
                    next_frontier.append(e.target)

            frontier = next_frontier

        return {
            "nodes": list(nodes.values()),
            "edges": edges,
        }

    # -------------------------
    # NOVO: EDGE QUERY
    # -------------------------
    def get_edges_by_type(self, edge_type: str):
        return self.edges_by_type.get(edge_type, [])

    # -------------------------
    # TRACE COMPLETO
    # -------------------------
    def trace_full(self, node_id: str):
        """
        Visão completa: estrutural + semântica.
        """

        return {
            "node": self.get_node(node_id),
            "trace": self.trace(node_id),
            "semantic": {
                "calls": self.semantic_trace(node_id, status="RESOLVED"),
                "runtime": self.semantic_trace(node_id, status="RUNTIME_APPROXIMATION"),
            },
        }
