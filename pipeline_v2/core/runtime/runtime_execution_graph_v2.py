# pipeline_v2/core/runtime/runtime_execution_graph_v2.py

from typing import Dict, List, Any, Optional  # , Set

# from collections import defaultdict


class RuntimeExecutionGraphV2:
    """
    Runtime Execution Graph V2

    Simulates execution flow over a static graph.

    NOT real execution.
    Structural runtime approximation.
    """

    def __init__(self, graph_core):
        self.graph = graph_core

        # runtime state per node
        self.node_state: Dict[str, str] = {}

        # execution timeline
        self.execution_trace: List[Dict[str, Any]] = []

        # runtime edges
        self.runtime_edges: List[Dict[str, Any]] = []

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def execute(self, entry_node: str, max_depth: int = 3) -> Dict[str, Any]:

        visited = set()
        frontier = [entry_node]

        depth = 0

        while frontier and depth < max_depth:

            next_frontier = []

            for node_id in frontier:

                if node_id in visited:
                    continue

                visited.add(node_id)

                self._set_state(node_id, "EXECUTING")

                edges = self.graph.edges_by_source.get(node_id, [])

                for edge in edges:

                    self._register_runtime_edge(edge, "TRIGGERED")

                    self.execution_trace.append(
                        {
                            "from": edge.get("source"),
                            "to": edge.get("target"),
                            "type": edge.get("type"),
                            "state": "PROPAGATED",
                        }
                    )

                    next_frontier.append(edge.get("target"))

                self._set_state(node_id, "COMPLETED")

            frontier = next_frontier
            depth += 1

        return {
            "states": self.node_state,
            "trace": self.execution_trace,
            "runtime_edges": self.runtime_edges,
        }

    # =====================================================
    # STATE MANAGEMENT
    # =====================================================

    def _set_state(self, node_id: str, state: str):

        self.node_state[node_id] = state

    # =====================================================
    # RUNTIME EDGE REGISTRY
    # =====================================================

    def _register_runtime_edge(self, edge: Dict[str, Any], state: str):

        self.runtime_edges.append(
            {
                "edge_id": edge.get("id"),
                "source": edge.get("source"),
                "target": edge.get("target"),
                "state": state,
            }
        )

    # =====================================================
    # QUERY RUNTIME STATE
    # =====================================================

    def get_node_state(self, node_id: str) -> Optional[str]:

        return self.node_state.get(node_id)

    def get_trace(self) -> List[Dict[str, Any]]:

        return self.execution_trace

    # =====================================================
    # ANALYSIS LAYER (FUTURE RAG)
    # =====================================================

    def execution_path(self, node_id: str) -> List[Dict[str, Any]]:

        return [t for t in self.execution_trace if t.get("from") == node_id]
