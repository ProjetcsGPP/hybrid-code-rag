# pipeline_v2/core/graph/graph_core.py

from collections import defaultdict
from typing import Dict, List, Optional, Set

from .graph_store import GraphStoreV2
from .graph_types import GraphNodeV2, GraphEdgeV2

from pipeline_v2.core.audit.graph_mutation_auditor_v2 import MutationEvent
from pipeline_v2.core.graph.boundary.graph_boundary_enforcer_v2 import (
    GraphBoundaryEnforcerV2,
)


class GraphCoreV2:
    """
    GraphCoreV2 - ENFORCED VERSION

    Agora atua como:
    - identity gatekeeper
    - deduplication guard
    - structural consistency enforcer
    """

    def __init__(self, mutation_auditor=None):

        self.mutation_auditor = mutation_auditor

        self.boundary = GraphBoundaryEnforcerV2()

        self.store = GraphStoreV2()

        self.edges_by_source: Dict[str, List[GraphEdgeV2]] = defaultdict(list)
        self.edges_by_target: Dict[str, List[GraphEdgeV2]] = defaultdict(list)
        self.edges_by_type: Dict[str, List[GraphEdgeV2]] = defaultdict(list)

        # -------------------------------------------------
        # NEW: ID REGISTRY (ENFORCEMENT CORE)
        # -------------------------------------------------

        self._node_ids: Set[str] = set()
        self._edge_ids: Set[str] = set()

        self._external_node_ids: Set[str] = set()

    def set_mutation_auditor(self, auditor):
        self.mutation_auditor = auditor

    def _ensure_node_exists(self, node_id: str):

        # HARD BOUNDARY RULE: no dirty nodes in graph core
        if node_id.startswith("UNRESOLVED::"):
            return None

        # external nodes são aceitos, mas só via lazy materialization

        existing = self.store.get_node(node_id)

        if existing:
            return existing

        # -------------------------------------------------
        # LAZY EXTERNAL MATERIALIZATION
        # -------------------------------------------------

        if node_id.startswith("external::"):

            if node_id in self._external_node_ids:
                return self.store.get_node(node_id)

            external_node = GraphNodeV2(
                id=node_id,
                type="external",
                name=node_id.split("::")[-1],
                canonical=node_id,
                metadata={
                    "mode": "EXTERNAL",
                    "semantic_only": True,
                    "lazy_materialized": True,
                },
            )

            self._external_node_ids.add(node_id)

            self.add_node(external_node)

            return external_node

        return None

    # =====================================================
    # NODE ENFORCEMENT
    # =====================================================

    def add_node(self, node: GraphNodeV2):
        """
        Enforces:
        - unique node identity
        - canonical stability
        """
        if not self.boundary.allow_node(node.id, node):
            return

        if self.mutation_auditor:

            decision = self.mutation_auditor.audit(
                MutationEvent(
                    actor="GraphCoreV2",
                    operation="ADD_NODE",
                    entity=node,
                    source=node.id,
                    metadata=getattr(node, "metadata", {}),
                )
            )

            if decision["action"] == "BLOCK":
                return

        if node.id in self._node_ids:
            # node já existe → ignora duplicação estrutural
            return

        if not node.id:
            raise ValueError("Node ID cannot be empty")

        self._node_ids.add(node.id)

        if node.metadata.get("mode") == "EXTERNAL":
            self._external_node_ids.add(node.id)

        self.store.add_node(node)

    def get_node(self, node_id: str) -> Optional[GraphNodeV2]:
        return self.store.get_node(node_id)

    # =====================================================
    # EDGE ENFORCEMENT (CRÍTICO)
    # =====================================================

    def add_edge(self, edge: GraphEdgeV2):
        """
        Enforces:
        - deterministic identity uniqueness
        - source/target integrity
        - duplicate prevention
        """

        if not self.boundary.allow_edge(edge):
            return

        if self.mutation_auditor:

            decision = self.mutation_auditor.audit(
                MutationEvent(
                    actor="GraphCoreV2",
                    operation="ADD_EDGE",
                    entity=edge,
                    source=edge.source,
                    target=edge.target,
                    metadata=getattr(edge, "metadata", {}),
                )
            )

            if decision["action"] == "BLOCK":
                return

        # -------------------------------------------------
        # 1. VALIDATION: ID
        # -------------------------------------------------

        if not edge.id:
            raise ValueError("Edge ID cannot be empty")

        if edge.id in self._edge_ids:
            # duplicata semântica ou replay → ignorar
            return

        # -------------------------------------------------
        # 2. VALIDATION: SOURCE / TARGET
        # -------------------------------------------------

        if not hasattr(edge, "source") or not hasattr(edge, "target"):
            return

        if not edge.source or not edge.target:
            raise ValueError(f"Invalid edge endpoints: {edge}")

        source_node = self._ensure_node_exists(edge.source)
        target_node = self._ensure_node_exists(edge.target)

        print(
            "EDGE REJECTED",
            edge.id,
            edge.source,
            source_node,
            edge.target,
            target_node,
        )

        if not source_node or not target_node:
            return

        # -------------------------------------------------
        # 3. REGISTER ID (CRITICAL)
        # -------------------------------------------------

        self._edge_ids.add(edge.id)

        # -------------------------------------------------
        # 4. VALIDATION: UNRESOLVED TARGETS (BÁSICA)
        # -------------------------------------------------

        if not self.validate_edge(edge):
            return

        # -------------------------------------------------
        # 5. PERSISTENCE
        # -------------------------------------------------

        self.store.add_edge(edge)

        # -------------------------------------------------
        # 5. INDEXING (CONSISTENCY)
        # -------------------------------------------------

        self.edges_by_source[edge.source].append(edge)
        self.edges_by_target[edge.target].append(edge)
        self.edges_by_type[edge.type].append(edge)

    # =====================================================
    # TRACE (UNCHANGED)
    # =====================================================

    def trace(self, node_id: str):
        return {
            "from": (
                self.edges_by_source[node_id]
                if node_id in self.edges_by_source
                else []
            ),
            "to": (
                self.edges_by_target[node_id]
                if node_id in self.edges_by_target
                else []
            ),
        }

    # =====================================================
    # SEMANTIC TRACE (ENHANCED SAFETY)
    # =====================================================

    def semantic_trace(
        self,
        node_id: str,
        layer: Optional[str] = None,
        status: Optional[str] = None,
    ):
        edges = (
            self.edges_by_source[node_id]
            if node_id in self.edges_by_source
            else []
        )

        if layer:
            edges = [e for e in edges if getattr(e, "layer", None) == layer]

        if status:
            edges = [e for e in edges if getattr(e, "status", None) == status]

        return edges

    # =====================================================
    # SUBGRAPH (SAFE VERSION)
    # =====================================================

    def subgraph(self, node_id: str, depth: int = 1):
        visited = set()
        frontier = [node_id]

        nodes = {}
        edges = []

        for _ in range(depth):
            next_frontier = []

            for nid in frontier:
                if nid in visited:
                    continue

                visited.add(nid)

                node = self.store.get_node(nid)
                if node:
                    nodes[node.id] = node

                for e in (
                    self.edges_by_source[nid]
                    if nid in self.edges_by_source
                    else []
                ):
                    edges.append(e)
                    next_frontier.append(e.target)

            frontier = next_frontier

        return {
            "nodes": list(nodes.values()),
            "edges": edges,
        }

    # =====================================================
    # EDGE QUERY
    # =====================================================

    def get_edges(self):
        """
        Test-only safe accessor.
        Returns all persisted edges.
        """
        return list(self.store.edges.values())

    def get_edges_by_type(self, edge_type: str):
        return (
            self.edges_by_type[edge_type]
            if edge_type in self.edges_by_type
            else []
        )

    # =====================================================
    # FULL TRACE
    # =====================================================

    def trace_full(self, node_id: str):
        return {
            "node": self.get_node(node_id),
            "trace": self.trace(node_id),
            "semantic": {
                "calls": self.semantic_trace(node_id, status="RESOLVED"),
                "runtime": self.semantic_trace(
                    node_id,
                    status="RUNTIME_APPROXIMATION",
                ),
            },
        }

    # =====================================================
    # GRAPH VALIDATION (BÁSICA)
    # =====================================================
    def validate_edge(self, edge):

        if edge.source.startswith("UNRESOLVED::"):
            return False

        if edge.target.startswith("UNRESOLVED::"):
            return False

        # external NÃO é inválido (incremental graph assumption)
        # mas evita auto-loop lixo
        if edge.source == edge.target and edge.source.startswith("external::"):
            return False

        return True

    # =====================================================
    # GRAPH RESET (ENFORCED)
    # =====================================================
    def reset(self):

        self.store.nodes.clear()
        self.store.edges.clear()

        self.edges_by_source.clear()
        self.edges_by_target.clear()
        self.edges_by_type.clear()

        self._node_ids.clear()
        self._edge_ids.clear()

        self._external_node_ids.clear()
