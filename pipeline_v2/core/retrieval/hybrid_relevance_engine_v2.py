# pipeline_v2/core/retrieval/hybrid_relevance_engine_v2.py


from typing import List, Optional
from collections import defaultdict

from pipeline_v2.core.contract.graph_contracts import (
    RankedNodeV2,
    ReasoningResultV2,
    RuntimeExecutionResultV2,
)
from pipeline_v2.core.graph.graph_types import GraphEdgeV2, GraphNodeV2


class HybridRelevanceEngineV2:
    """
    Hybrid Relevance Engine V2

    Final ranking layer combining:
    - structural relevance
    - semantic relevance
    - runtime relevance
    - reasoning signals (risk/impact)
    """

    def __init__(self):
        pass

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def rank(
        self,
        nodes: List[GraphNodeV2],
        edges: List[GraphEdgeV2],
        runtime_trace: Optional[RuntimeExecutionResultV2] = None,
        reasoning: Optional[ReasoningResultV2] = None,
    ) -> List[RankedNodeV2]:

        scores = defaultdict(float)

        self._score_structural(edges, scores)
        self._score_semantic(edges, scores)
        self._score_runtime(runtime_trace, scores)
        self._score_reasoning(reasoning, scores)

        ranked = self._build_ranked_nodes(nodes, scores)

        return sorted(ranked, key=lambda x: x.score, reverse=True)

    # =====================================================
    # 1. STRUCTURAL SCORE
    # =====================================================

    def _score_structural(self, edges, scores):

        for e in edges:
            scores[e.source] += 0.1
            scores[e.target] += 0.2

    # =====================================================
    # 2. SEMANTIC SCORE
    # =====================================================

    def _score_semantic(self, edges, scores):

        for e in edges:

            if e.layer == "SEMANTIC":
                scores[e.source] += 0.5
                scores[e.target] += 0.7

            if e.status == "RESOLVED":
                scores[e.target] += 0.3

    # =====================================================
    # 3. RUNTIME SCORE
    # =====================================================

    def _score_runtime(self, runtime_trace, scores):

        if not runtime_trace:
            return

        for event in runtime_trace.trace:
            scores[event.source] += 0.3
            scores[event.target] += 0.4

    # =====================================================
    # 4. REASONING SCORE
    # =====================================================

    def _score_reasoning(self, reasoning, scores):

        if not reasoning:
            return

        for node, r in reasoning.risk_scores.items():
            scores[node] += r * 0.5

        for node, targets in reasoning.impact_analysis.items():
            scores[node] += len(targets) * 0.2

    # =====================================================
    # FINAL ASSEMBLY
    # =====================================================

    def _build_ranked_nodes(self, nodes, scores):

        result = []

        for n in nodes:

            nid = n.id

            result.append(
                RankedNodeV2(
                    id=nid,
                    name=n.name,
                    type=n.type,
                    score=scores[nid] if nid in scores else 0.0,
                )
            )

        return result
