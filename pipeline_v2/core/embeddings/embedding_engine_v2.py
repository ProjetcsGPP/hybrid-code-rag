# pipeline_v2/core/embeddings/embedding_engine_v2.py

from typing import Dict, List  # , Optional
import hashlib

from pipeline_v2.core.graph.graph_types import GraphEdgeV2, GraphNodeV2


class EmbeddingEngineV2:
    """
    Embedding Engine V2

    Bridge layer between symbolic graph and vector space.

    NÃO assume modelo externo ainda.
    Pode ser plugado em:
    - OpenAI embeddings
    - sentence-transformers
    - custom model
    """

    def __init__(self):
        self.node_embeddings: Dict[str, List[float]] = {}
        self.edge_embeddings: Dict[str, List[float]] = {}

    # =====================================================
    # NODE EMBEDDING
    # =====================================================

    def embed_node(self, node: GraphNodeV2) -> List[float]:

        key = node.id

        if key in self.node_embeddings:
            return self.node_embeddings[key]

        vector = self._fake_embedding(
            node.name,
            node.type,
            node.canonical,
        )

        self.node_embeddings[key] = vector
        return vector

    # =====================================================
    # EDGE EMBEDDING
    # =====================================================

    def embed_edge(self, edge: GraphEdgeV2) -> List[float]:

        key = edge.id

        if key in self.edge_embeddings:
            return self.edge_embeddings[key]

        vector = self._fake_embedding(
            edge.type,
            edge.metadata["dispatch"] if "dispatch" in edge.metadata else "",
            (
                edge.metadata["framework_hint"]
                if "framework_hint" in edge.metadata
                else ""
            ),
        )

        self.edge_embeddings[key] = vector
        return vector

    # =====================================================
    # GRAPH EMBEDDING (AGGREGATE)
    # =====================================================

    def embed_subgraph(self, nodes: List[GraphNodeV2]) -> List[float]:

        if not nodes:
            return []

        vectors = [self.embed_node(n) for n in nodes]

        # simple aggregation (v1)
        dim = len(vectors[0])
        aggregated = [0.0] * dim

        for v in vectors:
            for i in range(dim):
                aggregated[i] += v[i]

        return [x / len(vectors) for x in aggregated]

    # =====================================================
    # PLACEHOLDER EMBEDDING FUNCTION
    # =====================================================

    def _fake_embedding(self, *args: str) -> List[float]:

        seed = "|".join(args)
        h = hashlib.sha256(seed.encode()).hexdigest()

        # convert hash → deterministic vector
        return [
            (int(h[i : i + 4], 16) % 1000) / 1000.0  # noqa: E203
            for i in range(0, 32, 4)
        ]
