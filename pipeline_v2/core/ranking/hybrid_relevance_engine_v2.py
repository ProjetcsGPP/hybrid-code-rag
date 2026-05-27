# pipeline_v2/core/ranking/hybrid_relevance_engine_v2.py

from typing import Dict, Any, Optional  # , List


class HybridRelevanceEngineV2:
    """
    Hybrid Relevance Engine V2

    Multi-signal ranking system for graph nodes.

    Combines:
    - structural signals
    - semantic signals (future-ready)
    - contextual signals
    """

    def __init__(self, index, registry=None):
        self.index = index
        self.registry = registry

    # =====================================================
    # MAIN SCORE ENTRY
    # =====================================================

    def score_node(
        self,
        node_id: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:

        structural = self._structural_score(node_id)
        semantic = self._semantic_score(node_id)
        contextual = self._context_score(node_id, context or {})

        # -------------------------------------------------
        # WEIGHTED COMBINATION (v1 fixed weights)
        # -------------------------------------------------

        score = structural * 0.45 + semantic * 0.25 + contextual * 0.30

        return score

    # =====================================================
    # STRUCTURAL SCORE
    # =====================================================

    def _structural_score(self, node_id: str) -> float:

        neighborhood = self.index.get_neighborhood(node_id)

        if not neighborhood:
            return 0.0

        degree = len(neighborhood["direct_neighbors"])
        incoming = len(neighborhood["incoming_edges"])
        outgoing = len(neighborhood["outgoing_edges"])

        # normalized structural importance
        return float(degree * 0.5 + incoming * 0.25 + outgoing * 0.25)

    # =====================================================
    # SEMANTIC SCORE (PREPARADO PARA FUTURO)
    # =====================================================

    def _semantic_score(self, node_id: str) -> float:

        neighborhood = self.index.get_neighborhood(node_id)

        if not neighborhood:
            return 0.0

        score = 0.0

        # edge-based semantic hints
        for edge in neighborhood["outgoing_edges"]:

            # framework hint boost
            if edge.get("framework_hint"):
                score += 1.5

            # semantic ownership boost
            if edge.get("semantic_owner"):
                score += 1.0

            # dispatch type weighting
            dispatch = edge.get("dispatch")
            if dispatch == "SELF":
                score += 0.8
            elif dispatch == "FRAMEWORK":
                score += 1.2
            elif dispatch == "DIRECT":
                score += 0.5

        return score

    # =====================================================
    # CONTEXT SCORE
    # =====================================================

    def _context_score(
        self,
        node_id: str,
        context: Dict[str, Any],
    ) -> float:

        seed = context.get("seed")

        if not seed:
            return 0.0

        if seed == node_id:
            return 5.0  # direct match boost

        neighborhood = self.index.get_neighborhood(seed)

        if not neighborhood:
            return 0.0

        # proximity boost
        if node_id in neighborhood["direct_neighbors"]:
            return 2.5

        if node_id in neighborhood["expanded_neighbors"]:
            return 1.2

        return 0.0

    # =====================================================
    # NORMALIZATION HOOK (FUTURE EMBEDDINGS)
    # =====================================================

    def normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:

        if not scores:
            return {}

        max_score = max(scores.values())

        if max_score == 0:
            return scores

        return {k: v / max_score for k, v in scores.items()}
