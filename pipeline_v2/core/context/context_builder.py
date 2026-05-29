# pipeline_v2/core/context/context_builder.py

from .context_types import ContextNode, ContextEdge, GraphContext
from .context_ranker import GraphContextRankerV2


class GraphContextBuilderV2:

    def __init__(self, graph):

        self.graph = graph
        self.ranker = GraphContextRankerV2()

    # -------------------------
    # MAIN ENTRYPOINT
    # -------------------------
    def build(self, node_id: str, depth: int = 2) -> GraphContext:

        subgraph = self.graph.subgraph(node_id, depth)

        raw_nodes = subgraph["nodes"]
        raw_edges = subgraph["edges"]

        # -------------------------
        # RANKING
        # -------------------------
        ranked_nodes = self.ranker.rank_nodes(raw_nodes, node_id)
        ranked_edges = self.ranker.rank_edges(raw_edges)

        # -------------------------
        # CONVERSION
        # -------------------------
        nodes = [
            ContextNode(
                id=n.id,
                type=n.type,
                name=n.name,
                canonical=getattr(n, "canonical", ""),
                metadata=getattr(n, "metadata", {}),
            )
            for n, _ in ranked_nodes
        ]

        edges = [
            ContextEdge(
                id=e.id,
                source=e.source,
                target=e.target,
                type=e.type,
                layer=e.layer,
                status=e.status,
                confidence=getattr(e, "confidence", 1.0),
                metadata=getattr(e, "metadata", {}),
            )
            for e, _ in ranked_edges
        ]

        focus_node = self.graph.get_node(node_id)

        return GraphContext(
            focus_node=ContextNode(
                id=focus_node.id,
                type=focus_node.type,
                name=focus_node.name,
                canonical=getattr(focus_node, "canonical", ""),
                metadata=getattr(focus_node, "metadata", {}),
            ),
            nodes=nodes,
            edges=edges,
            semantic_trace=self.graph.trace_full(node_id),
            ranked_score={
                "nodes": {n.id: s for n, s in ranked_nodes},
                "edges": {e.id: s for e, s in ranked_edges},
            },
            metadata={
                "depth": depth,
                "engine": "GraphContextBuilderV2",
                "mode": "universal_rag_context",
            },
        )
