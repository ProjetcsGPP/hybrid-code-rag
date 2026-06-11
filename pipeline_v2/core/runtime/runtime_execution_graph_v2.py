# pipeline_v2/core/runtime/runtime_execution_graph_v2.py

from typing import Dict, List, Optional  # , Set

# from collections import defaultdict

from pipeline_v2.core.contract.graph_contracts import (
    RuntimeEdgeEventV2,
    RuntimeExecutionResultV2,
    RuntimeTraceEventV2,
)
from pipeline_v2.core.graph.graph_types import GraphEdgeV2


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
        self.execution_trace: List[RuntimeTraceEventV2] = []

        # runtime edges
        self.runtime_edges: List[RuntimeEdgeEventV2] = []

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def execute(self, entry_node: str, max_depth: int = 3) -> RuntimeExecutionResultV2:

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

                edges = (
                    self.graph.edges_by_source[node_id]
                    if node_id in self.graph.edges_by_source
                    else []
                )

                for edge in edges:

                    self._register_runtime_edge(edge, "TRIGGERED")

                    self.execution_trace.append(
                        RuntimeTraceEventV2(
                            source=edge.source,
                            target=edge.target,
                            type=edge.type,
                        )
                    )

                    next_frontier.append(edge.target)

                self._set_state(node_id, "COMPLETED")

            frontier = next_frontier
            depth += 1

        return RuntimeExecutionResultV2(
            states=self.node_state,
            trace=self.execution_trace,
            runtime_edges=self.runtime_edges,
        )

    # =====================================================
    # STATE MANAGEMENT
    # =====================================================

    def _set_state(self, node_id: str, state: str):

        self.node_state[node_id] = state

    # =====================================================
    # RUNTIME EDGE REGISTRY
    # =====================================================

    def _register_runtime_edge(self, edge: GraphEdgeV2, state: str):

        self.runtime_edges.append(
            RuntimeEdgeEventV2(
                edge_id=edge.id,
                source=edge.source,
                target=edge.target,
                state=state,
            )
        )

    # =====================================================
    # QUERY RUNTIME STATE
    # =====================================================

    def get_node_state(self, node_id: str) -> Optional[str]:

        return self.node_state[node_id] if node_id in self.node_state else None

    def get_trace(self) -> List[RuntimeTraceEventV2]:

        return self.execution_trace

    # =====================================================
    # ANALYSIS LAYER (FUTURE RAG)
    # =====================================================

    def execution_path(self, node_id: str) -> List[RuntimeTraceEventV2]:

        return [t for t in self.execution_trace if t.source == node_id]
