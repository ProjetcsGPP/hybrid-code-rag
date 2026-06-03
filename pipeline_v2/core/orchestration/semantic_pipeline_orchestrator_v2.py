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


class SemanticPipelineOrchestratorV2:

    def __init__(self, legacy_engine, graph_builder, symbol_index=None):

        self.adapter = LegacySemanticAdapterV2()
        self.normalizer = CanonicalSemanticNormalizerV2()

        self.legacy = legacy_engine
        self.graph_builder = graph_builder

        self.inheritance_resolver = InheritanceResolverV2(symbol_index=symbol_index)

        self.stabilizer = SemanticGraphStabilizerV2()

    def execute(self, ast_payload):

        # =================================================
        # 1. LEGACY (apenas hints crus)
        # =================================================
        legacy_output = self.legacy.analyze(ast_payload)

        # =================================================
        # 2. ADAPTER → CANONICAL FORMAT V2
        # =================================================
        adapted = self.adapter.adapt(legacy_output)

        # =================================================
        # 3. NORMALIZATION (SELF / SUPER / ORM REMOVAL)
        #    🔥 CAMADA MAIS IMPORTANTE DO PROJETO AGORA
        # =================================================
        adapted = self.normalizer.normalize(adapted)

        # =================================================
        # 4. INHERITANCE RESOLUTION (V2 DECIDE REAL TARGET)
        # =================================================
        inheritance_hints = legacy_output.get("inheritance_edges", [])

        adapted["inheritance_edges"] = self.inheritance_resolver.resolve(
            inheritance_hints
        )

        # =================================================
        # 5. GRAPH BUILD (SEM SEMÂNTICA DUPLICADA)
        # =================================================
        graph_result = self.graph_builder.build(adapted)

        # =================================================
        # 6. POST-STABILIZATION (SÓ ESTRUTURAL)
        # =================================================
        graph_result["edges"] = self.stabilizer.stabilize(graph_result.get("edges", []))

        return graph_result
