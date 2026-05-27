# pipeline_v2/core/semantic/semantic_graph_stabilizer_v2.py

from collections import defaultdict


class SemanticGraphStabilizerV2:
    """
    Responsável por estabilizar inconsistências semânticas no grafo.

    Resolve:
    - duplicação de edges com significados diferentes
    - conflitos de confidence
    - múltiplas interpretações do mesmo call
    """

    def __init__(self):
        self.edge_registry = defaultdict(list)

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def stabilize(self, edges):

        self.edge_registry.clear()

        self._index(edges)

        stabilized = []

        for key, group in self.edge_registry.items():
            stabilized.append(self._merge(group))

        return stabilized

    # =====================================================
    # INDEXING
    # =====================================================

    def _index(self, edges):

        for e in edges:
            key = self._key(e)
            self.edge_registry[key].append(e)

    # =====================================================
    # KEY STRATEGY (CRÍTICO)
    # =====================================================

    def _key(self, edge):

        return f"{edge.source}|{edge.target}|{edge.raw_call}"

    # =====================================================
    # MERGE LOGIC
    # =====================================================

    def _merge(self, group):

        if len(group) == 1:
            return group[0]

        # regra 1: maior confidence vence
        best = max(group, key=lambda e: getattr(e, "confidence", 0))

        # regra 2: funde metadata
        merged_metadata = {}

        for e in group:
            if hasattr(e, "metadata") and e.metadata:
                merged_metadata.update(e.metadata)

        best.metadata = merged_metadata

        return best
