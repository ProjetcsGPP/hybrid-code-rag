# pipeline_v2/core/retrieval/hybrid_relevance_engine_v2.py


from typing import Dict, List, Any
from collections import defaultdict


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
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        runtime_trace: Dict[str, Any] = None,
        reasoning: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:

        scores = defaultdict(float)

        self._score_structural(edges, scores)
        self._score_semantic(edges, scores)
        self._score_runtime(runtime_trace, scores)
        self._score_reasoning(reasoning, scores)

        ranked = self._build_ranked_nodes(nodes, scores)

        return sorted(ranked, key=lambda x: x["score"], reverse=True)

    # =====================================================
    # 1. STRUCTURAL SCORE
    # =====================================================

    def _score_structural(self, edges, scores):

        for e in edges:
            scores[e.get("source")] += 0.1
            scores[e.get("target")] += 0.2

    # =====================================================
    # 2. SEMANTIC SCORE
    # =====================================================

    def _score_semantic(self, edges, scores):

        for e in edges:

            if e.get("layer") == "SEMANTIC":
                scores[e.get("source")] += 0.5
                scores[e.get("target")] += 0.7

            if e.get("status") == "RESOLVED":
                scores[e.get("target")] += 0.3

    # =====================================================
    # 3. RUNTIME SCORE
    # =====================================================

    def _score_runtime(self, runtime_trace, scores):

        if not runtime_trace:
            return

        trace = runtime_trace.get("trace", [])

        for event in trace:
            scores[event.get("from")] += 0.3
            scores[event.get("to")] += 0.4

    # =====================================================
    # 4. REASONING SCORE
    # =====================================================

    def _score_reasoning(self, reasoning, scores):

        if not reasoning:
            return

        risk = reasoning.get("risk_scores", {})
        impact = reasoning.get("impact_analysis", {})

        for node, r in risk.items():
            scores[node] += r * 0.5

        for node, targets in impact.items():
            scores[node] += len(targets) * 0.2

    # =====================================================
    # FINAL ASSEMBLY
    # =====================================================

    def _build_ranked_nodes(self, nodes, scores):

        result = []

        for n in nodes:

            nid = n.get("id")

            result.append(
                {
                    "id": nid,
                    "name": n.get("name"),
                    "type": n.get("type"),
                    "score": scores.get(nid, 0.0),
                }
            )

        return result
