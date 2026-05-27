# pipeline_v2/core/indexing/semantic_index_engine_v2.py

from collections import defaultdict
from typing import Dict, List, Set, Any, Optional


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
        self.incoming: Dict[str, List[dict]] = defaultdict(list)
        self.outgoing: Dict[str, List[dict]] = defaultdict(list)

        # node → semantic neighborhood cache
        self.neighborhood_cache: Dict[str, Dict[str, Any]] = {}

    # =====================================================
    # BUILD INDEX
    # =====================================================

    def build(
        self,
        nodes: List[dict],
        edges: List[dict],
    ):

        # normalize node IDs via registry (se existir)
        if self.registry:
            nodes = self._resolve_nodes(nodes)

        # -------------------------------------------------
        # STEP 1: EDGE PROCESSING
        # -------------------------------------------------

        for edge in edges:

            source = edge.get("source")
            target = edge.get("target")

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

            node_id = node.get("id")
            if not node_id:
                continue

            self.neighborhood_cache[node_id] = self._build_neighborhood(node_id)

    # =====================================================
    # NEIGHBORHOOD BUILDER
    # =====================================================

    def _build_neighborhood(self, node_id: str) -> Dict[str, Any]:

        direct_neighbors = self.adjacency.get(node_id, set())

        incoming = self.incoming.get(node_id, [])
        outgoing = self.outgoing.get(node_id, [])

        # categorize neighbors by depth (simple v1 heuristic)
        expanded = set(direct_neighbors)

        for n in list(direct_neighbors):
            expanded.update(self.adjacency.get(n, set()))

        return {
            "node_id": node_id,
            "direct_neighbors": list(direct_neighbors),
            "expanded_neighbors": list(expanded),
            "incoming_edges": incoming,
            "outgoing_edges": outgoing,
        }

    # =====================================================
    # QUERY API (FUTURE RAG USE)
    # =====================================================

    def get_neighborhood(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self.neighborhood_cache.get(node_id)

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

                next_frontier.update(self.adjacency.get(n, set()))

            frontier = next_frontier

        return visited

    # =====================================================
    # RANKING SUPPORT (BASE HOOK ONLY)
    # =====================================================

    def score_relevance(self, node_id: str) -> float:

        neighbors = len(self.adjacency.get(node_id, []))
        incoming = len(self.incoming.get(node_id, []))
        outgoing = len(self.outgoing.get(node_id, []))

        # simple structural importance heuristic (v1)
        return float(neighbors * 0.4 + incoming * 0.3 + outgoing * 0.3)

    # =====================================================
    # REGISTRY RESOLUTION
    # =====================================================

    def _resolve_nodes(self, nodes):

        resolved = []

        for n in nodes:

            canonical = n.get("canonical")

            if self.registry and canonical:
                reg = self.registry.get_by_canonical(canonical)

                if reg:
                    n["id"] = reg["symbol_id"]

            resolved.append(n)

        return resolved
