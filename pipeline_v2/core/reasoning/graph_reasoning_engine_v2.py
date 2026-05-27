# pipeline_v2/core/reasoning/graph_reasoning_engine_v2.py

from typing import Dict, List, Any, Set
from collections import defaultdict


class GraphReasoningEngineV2:
    """
    Graph Reasoning Engine V2

    Final reasoning layer over semantic + runtime + structural graph.

    Responsibilities:
    - impact analysis
    - path reasoning
    - risk scoring
    - intent inference (advanced)
    """

    def __init__(self, graph_core):
        self.graph = graph_core

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def reason(self, analysis_input: Dict[str, Any]) -> Dict[str, Any]:

        nodes = analysis_input.get("nodes", [])
        edges = analysis_input.get("edges", [])

        impact = self._impact_analysis(edges)
        critical = self._critical_nodes(edges)
        paths = self._reason_paths(edges)
        risk = self._risk_scoring(nodes, edges)

        intent = self._infer_system_intent(impact, risk, paths)

        return {
            "impact_analysis": impact,
            "critical_nodes": critical,
            "reasoned_paths": paths,
            "risk_scores": risk,
            "inferred_intent": intent,
        }

    # =====================================================
    # 1. IMPACT ANALYSIS
    # =====================================================

    def _impact_analysis(self, edges: List[Dict[str, Any]]) -> Dict[str, List[str]]:

        impact_map = defaultdict(list)

        for e in edges:
            src = e.get("source")
            tgt = e.get("target")

            impact_map[src].append(tgt)

        return dict(impact_map)

    # =====================================================
    # 2. CRITICAL NODES
    # =====================================================

    def _critical_nodes(self, edges: List[Dict[str, Any]]) -> Set[str]:

        dependency_count = defaultdict(int)

        for e in edges:
            dependency_count[e.get("target")] += 1

        return {node for node, count in dependency_count.items() if count > 2}

    # =====================================================
    # 3. PATH REASONING
    # =====================================================

    def _reason_paths(self, edges: List[Dict[str, Any]]) -> List[List[str]]:

        graph = defaultdict(list)

        for e in edges:
            graph[e.get("source")].append(e.get("target"))

        paths = []

        for src in graph:
            for mid in graph[src]:
                paths.append([src, mid])

        return paths

    # =====================================================
    # 4. RISK SCORING
    # =====================================================

    def _risk_scoring(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
    ) -> Dict[str, float]:

        risk = defaultdict(float)

        # node risk based on connectivity
        for e in edges:
            risk[e.get("source")] += 0.1
            risk[e.get("target")] += 0.2

        # normalize
        return {k: min(v, 1.0) for k, v in risk.items()}

    # =====================================================
    # 5. INTENT INFERENCE (ADVANCED)
    # =====================================================

    def _infer_system_intent(
        self,
        impact: Dict[str, List[str]],
        risk: Dict[str, float],
        paths: List[List[str]],
    ) -> str:

        high_impact_nodes = len(impact)
        high_risk_nodes = len([k for k, v in risk.items() if v > 0.5])
        path_complexity = len(paths)

        # -------------------------------------------------
        # HEURISTIC DECISION MODEL
        # -------------------------------------------------

        if high_risk_nodes > 5:
            return "RISK_AWARE_SYSTEM"

        if path_complexity > 20:
            return "PIPELINE_ORIENTED_SYSTEM"

        if high_impact_nodes > 10:
            return "HIGH_COUPLING_ARCHITECTURE"

        return "STABLE_LOW_COMPLEXITY_SYSTEM"
