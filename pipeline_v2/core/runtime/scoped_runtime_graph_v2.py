# pipeline_v2/core/runtime/scoped_runtime_graph_v2.py

from collections import defaultdict

from pipeline_v2.core.graph.graph_types import (
    GraphNodeV2,
    GraphEdgeV2,
)


class ScopedRuntimeGraphV2:
    """
    Runtime graph isolado por context_id.

    Evita colisão semântica entre:
    - projetos
    - branches
    - repositórios
    - workspaces
    """

    def __init__(self):

        self.context_nodes = defaultdict(dict)
        self.context_edges = defaultdict(dict)

    # =====================================================
    # NODES
    # =====================================================

    def add_node(
        self,
        context_id: str,
        node: GraphNodeV2,
    ):

        self.context_nodes[context_id][node.id] = node

    def get_node(
        self,
        context_id: str,
        node_id: str,
    ):

        return self.context_nodes.get(
            context_id,
            {},
        ).get(node_id)

    def get_nodes(
        self,
        context_id: str,
    ):

        return list(
            self.context_nodes.get(
                context_id,
                {},
            ).values()
        )

    # =====================================================
    # EDGES
    # =====================================================

    def add_edge(
        self,
        context_id: str,
        edge: GraphEdgeV2,
    ):

        self.context_edges[context_id][edge.id] = edge

    def get_edge(
        self,
        context_id: str,
        edge_id: str,
    ):

        return self.context_edges.get(
            context_id,
            {},
        ).get(edge_id)

    def get_edges(
        self,
        context_id: str,
    ):

        return list(
            self.context_edges.get(
                context_id,
                {},
            ).values()
        )

    # =====================================================
    # CONTEXT
    # =====================================================

    def clear_context(
        self,
        context_id: str,
    ):

        self.context_nodes.pop(context_id, None)
        self.context_edges.pop(context_id, None)

    def has_context(
        self,
        context_id: str,
    ):

        return context_id in self.context_nodes

    def stats(
        self,
        context_id: str,
    ):

        return {
            "nodes": len(
                self.context_nodes.get(
                    context_id,
                    {},
                )
            ),
            "edges": len(
                self.context_edges.get(
                    context_id,
                    {},
                )
            ),
        }
