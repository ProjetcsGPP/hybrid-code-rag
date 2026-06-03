# pipeline_v2/application/runtime_context.py

from dataclasses import dataclass

from pipeline_v2.core.identity.identity_registry import (
    IdentityRegistryV2,
)

from pipeline_v2.core.graph.graph_core import (
    GraphCoreV2,
)

from pipeline_v2.core.audit.graph_mutation_auditor_v2 import (
    GraphMutationAuditorV2,
)


@dataclass
class RuntimeContextV2:

    # Runtime boundary oficial do CODE-RAG V2.
    #
    # Responsável por encapsular:
    # - identity registry
    # - graph runtime
    # - mutation auditor
    #
    # Objetivos:
    # - isolamento de execução
    # - replay determinístico
    # - runtime incremental controlado
    # - eliminação de singleton contamination

    identity_registry: IdentityRegistryV2
    graph_runtime: GraphCoreV2
    mutation_auditor: GraphMutationAuditorV2

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):
        """
        Reset transacional completo do runtime.

        IMPORTANTE:
        Deve limpar TODO estado mutável associado
        ao runtime atual.
        """

        # -------------------------
        # GRAPH
        # -------------------------

        self.graph_runtime.reset()

        # -------------------------
        # IDENTITY REGISTRY
        # -------------------------

        self.identity_registry.clear()

    # =====================================================
    # STATS
    # =====================================================

    def stats(self):

        graph_nodes = len(self.graph_runtime.store.nodes)
        graph_edges = len(self.graph_runtime.store.edges)

        registry_stats = self.identity_registry.stats()

        return {
            "graph": {
                "nodes": graph_nodes,
                "edges": graph_edges,
            },
            "registry": registry_stats,
        }
