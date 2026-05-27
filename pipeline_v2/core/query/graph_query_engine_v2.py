# pipeline_v2/core/query/graph_query_engine_v2.py

from typing import Dict, List, Any, Set  # , Optional


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

    def query(self, query: Dict[str, Any]) -> Dict[str, Any]:
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

        start = query.get("start")
        depth = query.get("depth", 1)

        edges = self._traverse(start, depth)

        filtered_edges = self._apply_filters(edges, query)

        nodes = self._extract_nodes(filtered_edges)

        return {
            "nodes": nodes,
            "edges": filtered_edges,
        }

    # =====================================================
    # TRAVERSAL ENGINE
    # =====================================================

    def _traverse(self, start: str, depth: int) -> List[Dict[str, Any]]:

        visited: Set[str] = set()
        frontier = [start]

        collected_edges = []

        for _ in range(depth):

            next_frontier = []

            for node_id in frontier:

                if node_id in visited:
                    continue

                visited.add(node_id)

                edges = self.graph.edges_by_source.get(node_id, [])

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
        edges: List[Dict[str, Any]],
        query: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        edge_type = query.get("edge_type")
        layer = query.get("layer")
        status = query.get("status")
        framework_hint = query.get("framework_hint")

        result = []

        for e in edges:

            if edge_type and e.get("type") != edge_type:
                continue

            if layer and e.get("layer") != layer:
                continue

            if status and e.get("status") != status:
                continue

            if framework_hint and e.get("framework_hint") != framework_hint:
                continue

            result.append(e)

        return result

    # =====================================================
    # NODE EXTRACTION
    # =====================================================

    def _extract_nodes(self, edges: List[Dict[str, Any]]) -> List[str]:

        nodes = set()

        for e in edges:
            nodes.add(e.get("source"))
            nodes.add(e.get("target"))

        return list(nodes)

    # =====================================================
    # HIGH LEVEL QUERIES
    # =====================================================

    def neighbors(self, node_id: str, depth: int = 1) -> Dict[str, Any]:

        return self.query({"start": node_id, "depth": depth})

    def calls(self, node_id: str) -> Dict[str, Any]:

        return self.query({"start": node_id, "depth": 1, "edge_type": "CALLS"})

    def semantic_subgraph(self, node_id: str) -> Dict[str, Any]:

        return self.query({"start": node_id, "depth": 2, "layer": "SEMANTIC"})
