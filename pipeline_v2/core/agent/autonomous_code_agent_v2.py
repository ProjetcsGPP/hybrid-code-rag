# pipeline_v2/core/agent/autonomous_code_agent_v2.py

from typing import Dict, Any

from pipeline_v2.core.contract.graph_contracts import GraphAnalysisInputV2


class AutonomousCodeAgentV2:
    """
    Autonomous Code Agent V2

    Uses full Graph-RAG stack to reason and propose actions.
    """

    def __init__(
        self,
        query_engine,
        runtime_engine,
        trace_analyzer,
        reasoning_engine,
        relevance_engine,
    ):
        self.query_engine = query_engine
        self.runtime_engine = runtime_engine
        self.trace_analyzer = trace_analyzer
        self.reasoning_engine = reasoning_engine
        self.relevance_engine = relevance_engine

    # =====================================================
    # MAIN ENTRY
    # =====================================================

    def analyze(self, node_id: str) -> Dict[str, Any]:

        # 1. GRAPH QUERY
        subgraph = self.query_engine.semantic_subgraph(node_id)

        # 2. RUNTIME SIMULATION
        runtime = self.runtime_engine.execute(node_id)

        # 3. TRACE ANALYSIS
        trace_analysis = self.trace_analyzer.analyze(runtime)

        # 4. REASONING
        reasoning = self.reasoning_engine.reason(
            GraphAnalysisInputV2(nodes=subgraph.nodes, edges=subgraph.edges)
        )

        # 5. HYBRID RANKING
        ranking = self.relevance_engine.rank(
            nodes=subgraph.nodes,
            edges=subgraph.edges,
            runtime_trace=runtime,
            reasoning=reasoning,
        )

        return {
            "subgraph": subgraph,
            "runtime": runtime,
            "trace_analysis": trace_analysis,
            "reasoning": reasoning,
            "ranking": ranking,
        }
