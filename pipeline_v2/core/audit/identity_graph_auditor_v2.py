# pipeline_v2/core/audit/identity_graph_auditor_v2.py

from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, List


@dataclass
class IdentityReport:
    total_nodes: int
    registry_nodes: int
    graph_nodes: int

    missing_in_graph: List[str]
    orphan_graph_nodes: List[str]

    inferred_nodes: List[str]
    external_nodes: List[str]
    strict_nodes: List[str]

    drift_score: float
    identity_entropy: float

    by_source_distribution: Dict[str, int]


class IdentityGraphAuditorV2:
    """
    Auditor completo de consistência de identidade.

    Analisa:
    - Registry vs Graph
    - origem de identidade (mode)
    - drift estrutural
    - distribuição semântica
    """

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def audit(self, identity_registry, graph_store):

        registry_ids = {
            rid
            for rid in identity_registry.by_id.keys()
            if not self._is_relationship_identity(rid)
        }

        graph_nodes = graph_store.nodes

        graph_ids = set(graph_nodes.keys())

        # -------------------------------------------------
        # DRIFT CORE
        # -------------------------------------------------
        missing_in_graph = list(registry_ids - graph_ids)
        orphan_graph_nodes = list(graph_ids - registry_ids)

        # -------------------------------------------------
        # CLASSIFICATION
        # -------------------------------------------------
        inferred = []
        external = []
        strict = []

        by_source = defaultdict(int)

        for node in graph_nodes.values():

            metadata = getattr(node, "metadata", {}) or {}
            mode = metadata["mode"] if "mode" in metadata else "STRICT"

            by_source[mode] += 1

            if mode == "INFERRED":
                inferred.append(node.id)

            elif mode == "EXTERNAL":
                external.append(node.id)

            else:
                strict.append(node.id)

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------
        total = len(graph_ids) or 1

        drift_score = len(missing_in_graph) / total

        identity_entropy = self._compute_entropy(by_source, total)

        # -------------------------------------------------
        # REPORT
        # -------------------------------------------------
        return IdentityReport(
            total_nodes=len(graph_ids),
            registry_nodes=len(registry_ids),
            graph_nodes=len(graph_ids),
            missing_in_graph=missing_in_graph,
            orphan_graph_nodes=orphan_graph_nodes,
            inferred_nodes=inferred,
            external_nodes=external,
            strict_nodes=strict,
            drift_score=drift_score,
            identity_entropy=identity_entropy,
            by_source_distribution=dict(by_source),
        )

    # =====================================================
    # ENTROPY (STRUCTURAL COMPLEXITY SCORE)
    # =====================================================

    def _compute_entropy(self, distribution: Dict[str, int], total: int):
        import math

        entropy = 0.0

        for count in distribution.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    def _is_relationship_identity(self, identity_id: str):

        markers = [
            "::CALLS::",
            "::FRAMEWORK_CALL::",
            "::IMPORTS::",
            "::EXTENDS::",
            "::BELONGS_TO::",
        ]

        return any(marker in identity_id for marker in markers)
