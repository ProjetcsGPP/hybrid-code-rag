# pipeline_v2/core/reasoning/graph_reasoning_engine_v2.py

from typing import Dict, List, Set
from collections import defaultdict

from pipeline_v2.core.contract.graph_contracts import (
    GraphAnalysisInputV2,
    ReasoningResultV2,
)
from pipeline_v2.core.graph.graph_types import GraphEdgeV2, GraphNodeV2


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

    def reason(self, analysis_input: GraphAnalysisInputV2) -> ReasoningResultV2:

        nodes = analysis_input.nodes
        edges = analysis_input.edges

        impact = self._impact_analysis(edges)
        critical = self._critical_nodes(edges)
        paths = self._reason_paths(edges)
        risk = self._risk_scoring(nodes, edges)

        intent = self._infer_system_intent(impact, risk, paths)

        return ReasoningResultV2(
            impact_analysis=impact,
            risk_scores=risk,
            critical_nodes=frozenset(critical),
            reasoned_paths=paths,
            inferred_intent=intent,
        )

    # =====================================================
    # 1. IMPACT ANALYSIS
    # =====================================================

    def _impact_analysis(self, edges: List[GraphEdgeV2]) -> Dict[str, List[str]]:

        impact_map = defaultdict(list)

        for e in edges:
            src = e.source
            tgt = e.target

            impact_map[src].append(tgt)

        return dict(impact_map)

    # =====================================================
    # 2. CRITICAL NODES
    # =====================================================

    def _critical_nodes(self, edges: List[GraphEdgeV2]) -> Set[str]:

        dependency_count = defaultdict(int)

        for e in edges:
            dependency_count[e.target] += 1

        return {node for node, count in dependency_count.items() if count > 2}

    # =====================================================
    # 3. PATH REASONING
    # =====================================================

    def _reason_paths(self, edges: List[GraphEdgeV2]) -> List[List[str]]:

        graph = defaultdict(list)

        for e in edges:
            graph[e.source].append(e.target)

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
        nodes: List[GraphNodeV2],
        edges: List[GraphEdgeV2],
    ) -> Dict[str, float]:

        risk = defaultdict(float)

        # node risk based on connectivity
        for e in edges:
            risk[e.source] += 0.1
            risk[e.target] += 0.2

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
