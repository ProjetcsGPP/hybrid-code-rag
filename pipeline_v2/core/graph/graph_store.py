# pipeline_v2/core/graph/graph_store.py

from typing import Dict

from .graph_types import (
    GraphNodeV2,
    GraphEdgeV2,
)


class GraphStoreV2:

    def __init__(self):

        self.nodes: Dict[str, GraphNodeV2] = {}
        self.edges: Dict[str, GraphEdgeV2] = {}

    # =========================================
    # NODE OPS
    # =========================================

    def add_node(self, node: GraphNodeV2):

        self.nodes[node.id] = node

    def get_node(self, node_id: str):

        return self.nodes.get(node_id)

    def get_nodes(self):

        return list(self.nodes.values())

    # =========================================
    # EDGE OPS
    # =========================================

    def add_edge(self, edge: GraphEdgeV2):

        self.edges[edge.id] = edge

    def get_edge(self, edge_id: str):

        return self.edges.get(edge_id)

    def get_edges(self):

        return list(self.edges.values())

    def get_edges_from(self, node_id: str):

        return [e for e in self.edges.values() if e.source == node_id]

    def get_edges_to(self, node_id: str):

        return [e for e in self.edges.values() if e.target == node_id]

    # =========================================
    # DEBUG
    # =========================================

    def summary(self):

        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "density": len(self.edges) / max(len(self.nodes), 1),
        }
