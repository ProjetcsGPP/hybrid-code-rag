# pipeline_v2/core/indexing/semantic_index_engine_v2.py

from collections import defaultdict
from typing import Dict, List, Set, Optional

from pipeline_v2.core.contract.graph_contracts import GraphSubgraphV2
from pipeline_v2.core.graph.graph_types import GraphEdgeV2, GraphNodeV2


class SemanticIndexEngineV2:
    """
    Semantic Index Engine V2

    Builds semantic retrieval structures over a normalized graph.

    This is NOT a search engine.
    It is a semantic structuring layer.
    """

    def __init__(self, registry=None):
        self.registry = registry

        # node → neighbors (semantic adjacency)
        self.adjacency: Dict[str, Set[str]] = defaultdict(set)

        # node → incoming/outgoing categorization
        self.incoming: Dict[str, List[GraphEdgeV2]] = defaultdict(list)
        self.outgoing: Dict[str, List[GraphEdgeV2]] = defaultdict(list)
        self.nodes_by_id: Dict[str, GraphNodeV2] = {}

        # node → semantic neighborhood cache
        self.neighborhood_cache: Dict[str, GraphSubgraphV2] = {}

    # =====================================================
    # BUILD INDEX
    # =====================================================

    def build(
        self,
        nodes: List[GraphNodeV2],
        edges: List[GraphEdgeV2],
    ):

        # normalize node IDs via registry (se existir)
        if self.registry:
            nodes = self._resolve_nodes(nodes)

        # -------------------------------------------------
        # STEP 1: EDGE PROCESSING
        # -------------------------------------------------

        for edge in edges:

            source = edge.source
            target = edge.target

            if not source or not target:
                continue

            # adjacency (bidirectional semantic awareness)
            self.adjacency[source].add(target)
            self.adjacency[target].add(source)

            self.outgoing[source].append(edge)
            self.incoming[target].append(edge)

        # -------------------------------------------------
        # STEP 2: NEIGHBORHOOD BUILD
        # -------------------------------------------------

        for node in nodes:

            node_id = node.id
            if not node_id:
                continue

            self.nodes_by_id[node_id] = node
            self.neighborhood_cache[node_id] = self._build_neighborhood(node_id)

    # =====================================================
    # NEIGHBORHOOD BUILDER
    # =====================================================

    def _build_neighborhood(self, node_id: str) -> GraphSubgraphV2:

        direct_neighbors = (
            self.adjacency[node_id] if node_id in self.adjacency else set()
        )

        incoming = self.incoming[node_id] if node_id in self.incoming else []
        outgoing = self.outgoing[node_id] if node_id in self.outgoing else []

        # categorize neighbors by depth (simple v1 heuristic)
        expanded = set(direct_neighbors)

        for n in list(direct_neighbors):
            expanded.update(self.adjacency[n] if n in self.adjacency else set())

        neighborhood_nodes = [
            self.nodes_by_id[n] for n in expanded if n in self.nodes_by_id
        ]

        return GraphSubgraphV2(
            nodes=neighborhood_nodes,
            edges=incoming + outgoing,
        )

    # =====================================================
    # QUERY API (FUTURE RAG USE)
    # =====================================================

    def get_neighborhood(self, node_id: str) -> Optional[GraphSubgraphV2]:
        return (
            self.neighborhood_cache[node_id]
            if node_id in self.neighborhood_cache
            else None
        )

    # =====================================================
    # CONTEXT EXPANSION
    # =====================================================

    def expand_context(self, node_id: str, depth: int = 1) -> Set[str]:

        visited = set()
        frontier = {node_id}

        for _ in range(depth):
            next_frontier = set()

            for n in frontier:

                if n in visited:
                    continue

                visited.add(n)

                next_frontier.update(
                    self.adjacency[n] if n in self.adjacency else set()
                )

            frontier = next_frontier

        return visited

    # =====================================================
    # RANKING SUPPORT (BASE HOOK ONLY)
    # =====================================================

    def score_relevance(self, node_id: str) -> float:

        neighbors = len(self.adjacency[node_id] if node_id in self.adjacency else [])
        incoming = len(self.incoming[node_id] if node_id in self.incoming else [])
        outgoing = len(self.outgoing[node_id] if node_id in self.outgoing else [])

        # simple structural importance heuristic (v1)
        return float(neighbors * 0.4 + incoming * 0.3 + outgoing * 0.3)

    # =====================================================
    # REGISTRY RESOLUTION
    # =====================================================

    def _resolve_nodes(self, nodes):

        resolved = []

        for n in nodes:

            canonical = n.canonical

            if self.registry and canonical:
                reg = self.registry.get_by_canonical(canonical)

                if reg:
                    n.id = reg["symbol_id"]

            resolved.append(n)

        return resolved
