# pipeline_v2/core/ranking/hybrid_relevance_engine_v2.py

from typing import Dict, Optional

from pipeline_v2.core.contract.graph_contracts import RankingContextV2


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
        context: Optional[RankingContextV2] = None,
    ) -> float:

        structural = self._structural_score(node_id)
        semantic = self._semantic_score(node_id)
        contextual = self._context_score(node_id, context or RankingContextV2())

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

        degree = len(neighborhood.nodes)
        incoming = len([edge for edge in neighborhood.edges if edge.target == node_id])
        outgoing = len([edge for edge in neighborhood.edges if edge.source == node_id])

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
        for edge in neighborhood.edges:

            if edge.source != node_id:
                continue

            # framework hint boost
            if "framework_hint" in edge.metadata and edge.metadata["framework_hint"]:
                score += 1.5

            # semantic ownership boost
            if "semantic_owner" in edge.metadata and edge.metadata["semantic_owner"]:
                score += 1.0

            # dispatch type weighting
            dispatch = (
                edge.metadata["dispatch"] if "dispatch" in edge.metadata else None
            )
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
        context: RankingContextV2,
    ) -> float:

        seed = context.seed

        if not seed:
            return 0.0

        if seed == node_id:
            return 5.0  # direct match boost

        neighborhood = self.index.get_neighborhood(seed)

        if not neighborhood:
            return 0.0

        # proximity boost
        if any(node.id == node_id for node in neighborhood.nodes):
            return 2.5

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
