# pipeline_v2/core/query/graph_query_engine_v2.py

from typing import List, Set  # , Optional

from pipeline_v2.core.contract.graph_contracts import (
    GraphQueryContract,
    GraphSubgraphV2,
)
from pipeline_v2.core.graph.graph_types import GraphEdgeV2


class GraphQueryEngineV2:
    """
    Graph Query Engine V2

    Declarative query layer over GraphCoreV2.

    Responsibilities:
    - traversal queries
    - structural filtering
    - semantic filtering hooks
    - subgraph extraction
    """

    def __init__(self, graph_core):
        self.graph = graph_core

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def query(self, query: GraphQueryContract) -> GraphSubgraphV2:
        """
        Example query:

        {
            "start": "node_id",
            "depth": 2,
            "edge_type": "CALLS",
            "node_type": "function",
            "layer": "SEMANTIC",
            "status": "RESOLVED"
        }
        """

        start = query.start
        depth = query.depth

        edges = self._traverse(start, depth)

        filtered_edges = self._apply_filters(edges, query)

        nodes = self._extract_nodes(filtered_edges)

        return GraphSubgraphV2(
            nodes=[
                self.graph.store.nodes[node_id]
                for node_id in nodes
                if node_id in self.graph.store.nodes
            ],
            edges=filtered_edges,
        )

    # =====================================================
    # TRAVERSAL ENGINE
    # =====================================================

    def _traverse(self, start: str, depth: int) -> List[GraphEdgeV2]:

        visited: Set[str] = set()
        frontier = [start]

        collected_edges = []

        for _ in range(depth):

            next_frontier = []

            for node_id in frontier:

                if node_id in visited:
                    continue

                visited.add(node_id)

                edges = (
                    self.graph.edges_by_source[node_id]
                    if node_id in self.graph.edges_by_source
                    else []
                )

                for e in edges:
                    collected_edges.append(e)
                    next_frontier.append(e.target)

            frontier = next_frontier

        return collected_edges

    # =====================================================
    # FILTER ENGINE
    # =====================================================

    def _apply_filters(
        self,
        edges: List[GraphEdgeV2],
        query: GraphQueryContract,
    ) -> List[GraphEdgeV2]:

        edge_type = query.edge_type
        layer = query.layer
        status = query.status
        framework_hint = query.framework_hint

        result = []

        for e in edges:

            if edge_type and e.type != edge_type:
                continue

            if layer and e.layer != layer:
                continue

            if status and e.status != status:
                continue

            edge_framework_hint = (
                e.metadata["framework_hint"] if "framework_hint" in e.metadata else None
            )
            if framework_hint and edge_framework_hint != framework_hint:
                continue

            result.append(e)

        return result

    # =====================================================
    # NODE EXTRACTION
    # =====================================================

    def _extract_nodes(self, edges: List[GraphEdgeV2]) -> List[str]:

        nodes = set()

        for e in edges:
            nodes.add(e.source)
            nodes.add(e.target)

        return list(nodes)

    # =====================================================
    # HIGH LEVEL QUERIES
    # =====================================================

    def neighbors(self, node_id: str, depth: int = 1) -> GraphSubgraphV2:

        return self.query(GraphQueryContract(start=node_id, depth=depth))

    def calls(self, node_id: str) -> GraphSubgraphV2:

        return self.query(GraphQueryContract(start=node_id, depth=1, edge_type="CALLS"))

    def semantic_subgraph(self, node_id: str) -> GraphSubgraphV2:

        return self.query(GraphQueryContract(start=node_id, depth=2, layer="SEMANTIC"))
