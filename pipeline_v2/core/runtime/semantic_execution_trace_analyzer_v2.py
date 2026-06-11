# pipeline_v2/core/runtime/semantic_execution_trace_analyzer_v2.py

from typing import Dict, List  # , Set
from collections import defaultdict

from pipeline_v2.core.contract.graph_contracts import (
    ClassifiedRuntimeTraceEventV2,
    RuntimeExecutionResultV2,
    RuntimeTraceEventV2,
)


class SemanticExecutionTraceAnalyzerV2:
    """
    Semantic Execution Trace Analyzer V2

    Converts runtime execution traces into semantic meaning.

    INPUT:
        - runtime_execution_graph output

    OUTPUT:
        - semantic interpretation of execution behavior
    """

    def __init__(self):
        pass

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def analyze(self, runtime_output: RuntimeExecutionResultV2) -> Dict[str, object]:

        trace = runtime_output.trace

        classified = self._classify_flow(trace)
        patterns = self._detect_patterns(trace)
        semantics = self._infer_semantics(classified, patterns)

        return {
            "classified_trace": classified,
            "patterns": patterns,
            "semantic_summary": semantics,
        }

    # =====================================================
    # 1. FLOW CLASSIFICATION
    # =====================================================

    def _classify_flow(
        self,
        trace: List[RuntimeTraceEventV2],
    ) -> List[ClassifiedRuntimeTraceEventV2]:

        result = []

        for event in trace:

            flow_type = self._infer_flow_type(event)

            result.append(
                ClassifiedRuntimeTraceEventV2(
                    source=event.source,
                    target=event.target,
                    type=event.type,
                    state=event.state,
                    flow_type=flow_type,
                )
            )

        return result

    def _infer_flow_type(self, event: RuntimeTraceEventV2) -> str:

        edge_type = event.type

        if edge_type in ["CALLS"]:
            return "CONTROL_FLOW"

        if edge_type in ["IMPORTS"]:
            return "DEPENDENCY_FLOW"

        if edge_type in ["BINDS"]:
            return "DATA_BINDING_FLOW"

        return "UNKNOWN_FLOW"

    # =====================================================
    # 2. PATTERN DETECTION
    # =====================================================

    def _detect_patterns(self, trace: List[RuntimeTraceEventV2]) -> Dict[str, object]:

        outgoing = defaultdict(int)
        incoming = defaultdict(int)

        for event in trace:
            src = event.source
            tgt = event.target

            outgoing[src] += 1
            incoming[tgt] += 1

        fan_out = {k: v for k, v in outgoing.items() if v > 1}
        fan_in = {k: v for k, v in incoming.items() if v > 1}

        return {
            "fan_out_nodes": fan_out,
            "fan_in_nodes": fan_in,
            "total_events": len(trace),
        }

    # =====================================================
    # 3. SEMANTIC INFERENCE
    # =====================================================

    def _infer_semantics(
        self,
        classified: List[ClassifiedRuntimeTraceEventV2],
        patterns: Dict[str, object],
    ) -> Dict[str, str]:

        summary = {
            "intent": "UNKNOWN",
            "behavior_type": "UNKNOWN",
            "complexity": "LOW",
        }

        total = len(classified)

        control_flow = len([e for e in classified if e.flow_type == "CONTROL_FLOW"])

        dependency_flow = len(
            [e for e in classified if e.flow_type == "DEPENDENCY_FLOW"]
        )

        # -------------------------------------------------
        # INTENT INFERENCE (heuristic v1)
        # -------------------------------------------------

        if control_flow > dependency_flow:
            summary["intent"] = "EXECUTION_DRIVEN"

        if dependency_flow > control_flow:
            summary["intent"] = "STRUCTURE_DRIVEN"

        # -------------------------------------------------
        # BEHAVIOR TYPE
        # -------------------------------------------------

        if patterns["fan_out_nodes"]:
            summary["behavior_type"] = "DISTRIBUTED_DISPATCH"

        if patterns["fan_in_nodes"]:
            summary["behavior_type"] = "AGGREGATION_FLOW"

        # -------------------------------------------------
        # COMPLEXITY ESTIMATION
        # -------------------------------------------------

        if total > 50:
            summary["complexity"] = "HIGH"
        elif total > 15:
            summary["complexity"] = "MEDIUM"

        return summary
