# pipeline_v2/core/orchestration/semantic_pipeline_orchestrator_v2.py

from pipeline_v2.core.semantic.inheritance.inheritance_resolver_v2 import (
    InheritanceResolverV2,
)
from pipeline_v2.core.semantic.semantic_graph_stabilizer_v2 import (
    SemanticGraphStabilizerV2,
)

from pipeline_v2.core.semantic.legacy_semantic_adapter_v2 import LegacySemanticAdapterV2

from pipeline_v2.core.semantic.canonical_semantic_normalizer_v2 import (
    CanonicalSemanticNormalizerV2,
)

from pipeline_v2.core.closure.semantic_closure_loop import SemanticClosureLoopV2

from pipeline_v2.core.graph.graph_types import GraphEdgeV2

# from pipeline_v2.core.execution.pipeline_executor_v2 import PipelineExecutorV2


class SemanticPipelineOrchestratorV2:

    def __init__(
        self,
        legacy_engine,
        graph_builder,
        symbol_index=None,
        identity_registry=None,
        graph_core=None,
    ):

        self.adapter = LegacySemanticAdapterV2()
        self.normalizer = CanonicalSemanticNormalizerV2()

        self.legacy = legacy_engine
        self.graph_builder = graph_builder

        self.identity_registry = identity_registry
        self.graph_core = graph_core

        self.inheritance_resolver = InheritanceResolverV2(symbol_index=symbol_index)

        self.stabilizer = SemanticGraphStabilizerV2()

    def execute(self, ast_payload):

        legacy_output = self.legacy.analyze(ast_payload)

        adapted = self.adapter.adapt(legacy_output)

        adapted["edges"] = [
            GraphEdgeV2(
                id=e["id"],
                source=e["source"],
                target=e["target"],
                type=e["type"] if "type" in e else "CALL",
                layer=e["layer"] if "layer" in e else None,
                status=e["status"] if "status" in e else "RESOLVED",
                confidence=e["confidence"] if "confidence" in e else 1.0,
                metadata=e["metadata"] if "metadata" in e else {},
            )
            for e in (
                legacy_output["relationships"]
                if "relationships" in legacy_output
                else []
            )
        ]

        if "edges" in adapted:
            adapted["edges"] = self.stabilizer.stabilize(adapted["edges"])

        graph_result = self.graph_builder.build(adapted)

        for edge in graph_result.edges:
            self.graph_core.add_edge(edge)

        closure = SemanticClosureLoopV2(self.identity_registry, self.graph_core)
        closure.execute(graph_result.edges)

        return graph_result
