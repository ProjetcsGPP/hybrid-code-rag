# pipeline_v2/tests/fixtures/orchestrator_factory.py

from pipeline_v2.core.orchestration.semantic_pipeline_orchestrator_v2 import (
    SemanticPipelineOrchestratorV2,
)

from pipeline_v2.core.graph.graph_core import GraphCoreV2
from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2
from pipeline_v2.core.builder.graph_builder import GraphBuilderV2

# =====================================================
# REAL LEGACY ENGINE (mínimo válido para teste)
# =====================================================


class TestLegacyEngine:

    def analyze(self, ast_payload):
        return {
            "symbols": [
                {
                    "id": "service",
                    "name": "service",
                    "type": "module",
                    "canonical": "service",
                    "metadata": {},
                },
                {
                    "id": "repo",
                    "name": "repo",
                    "type": "module",
                    "canonical": "repo",
                    "metadata": {},
                },
            ],
            "relationships": [
                {
                    "id": "r1",
                    "source": "service",
                    "target": "repo",
                    "type": "CALL",
                    "layer": "APP",
                    "status": "RESOLVED",
                    "confidence": 1.0,
                    "metadata": {},
                }
            ],
            "inheritance_edges": [],
        }


# =====================================================
# ORCHESTRATOR FACTORY (CORRETO: função global)
# =====================================================


def build_orchestrator():

    identity_registry = IdentityRegistryV2()
    graph_core = GraphCoreV2()

    legacy_engine = TestLegacyEngine()

    graph_builder = GraphBuilderV2(
        identity_registry=identity_registry,
        graph_core=graph_core,
    )

    orchestrator = SemanticPipelineOrchestratorV2(
        legacy_engine=legacy_engine,
        graph_builder=graph_builder,
        symbol_index={},
        identity_registry=identity_registry,
        graph_core=graph_core,
    )

    return orchestrator
