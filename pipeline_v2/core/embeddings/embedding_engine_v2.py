# pipeline_v2/core/embeddings/embedding_engine_v2.py

from typing import Dict, List, Any  # , Optional
import hashlib


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

    def embed_node(self, node: Dict[str, Any]) -> List[float]:

        key = node.get("id")

        if key in self.node_embeddings:
            return self.node_embeddings[key]

        vector = self._fake_embedding(
            node.get("name", ""),
            node.get("type", ""),
            node.get("canonical", ""),
        )

        self.node_embeddings[key] = vector
        return vector

    # =====================================================
    # EDGE EMBEDDING
    # =====================================================

    def embed_edge(self, edge: Dict[str, Any]) -> List[float]:

        key = edge.get("id")

        if key in self.edge_embeddings:
            return self.edge_embeddings[key]

        vector = self._fake_embedding(
            edge.get("type", ""),
            edge.get("dispatch", ""),
            edge.get("framework_hint", ""),
        )

        self.edge_embeddings[key] = vector
        return vector

    # =====================================================
    # GRAPH EMBEDDING (AGGREGATE)
    # =====================================================

    def embed_subgraph(self, nodes: List[Dict[str, Any]]) -> List[float]:

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
