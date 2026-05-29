# pipeline_v2/core/relationship/relationship_core.py

from .relationship_factory import RelationshipFactoryV2
from .relationship_resolver import RelationshipResolverV2

from pipeline_v2.core.state.semantic_context import SemanticContextV2
from pipeline_v2.core.state.assignment_resolver import AssignmentResolverV2

from pipeline_v2.core.resolution.symbol_resolution_engine_v2 import (
    SymbolResolutionEngineV2,
)
from pipeline_v2.core.identity.identity_service_v2 import (
    IdentityServiceV2,
)
from pipeline_v2.core.identity.identity_mode import IdentityMode
from pipeline_v2.core.graph.graph_types import GraphNodeV2


class RelationshipCoreV2:
    """
    Relationship orchestration layer.

    Responsável apenas por:
    - semantic orchestration
    - relationship inference
    - relationship creation
    """

    def __init__(
        self,
        symbol_core=None,
        graph_core=None,
        identity_registry=None,
    ):

        self.symbol_core = symbol_core
        self.graph_core = graph_core

        # registry único de verdade
        if identity_registry is None:
            raise ValueError("RelationshipCoreV2 requires shared identity_registry")

        self.identity_registry = identity_registry

        self.identity = IdentityServiceV2(self.identity_registry)

        self.resolver = RelationshipResolverV2()

        self.resolution_engine = SymbolResolutionEngineV2(
            symbol_core=symbol_core,
            graph_core=graph_core,
            identity_registry=self.identity_registry,
        )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def process_chunk(
        self,
        chunk,
        symbol_table,
    ):

        relationships = []

        semantic_context = self._build_semantic_context(chunk)

        source = self.resolution_engine.resolve_source(
            chunk,
            symbol_table,
            self._chunk_id,
            self._chunk_metadata,
        )

        if not source:
            return relationships

        # 🔴 IMPORTANTE: não mutar source global
        resolved_source = self.identity.resolve(source)

        for raw_call in self._chunk_raw_calls(chunk):

            normalized_call = self.resolution_engine.normalize_call(raw_call)

            resolved = self.resolver.resolve_call(
                caller_symbol=resolved_source,
                raw_call=normalized_call["raw"],
                semantic_context=semantic_context,
            )

            semantic_data = resolved.get("semantic", {})

            target = self.resolution_engine.resolve_semantic_target(
                semantic_data,
                symbol_table,
            )

            if not target:
                target = self.resolution_engine.resolve_target(
                    normalized_call["raw"],
                    symbol_table,
                )

            if not target:
                continue

            resolved_target = self.identity.resolve(target)

            if resolved_target is None:
                resolved_target = f"external::{target}"

            # SOURCE identity handling (controlled)
            self._ensure_identity_node(str(resolved_source), IdentityMode.INFERRED)

            # TARGET identity handling (controlled)
            self._ensure_identity_node(str(resolved_target), IdentityMode.EXTERNAL)

            rel = RelationshipFactoryV2.create(
                source=str(resolved_source),
                target=str(resolved_target),
                type=resolved["relationship_type"],
                dispatch=resolved["dispatch"],
                raw_call=normalized_call["raw"],
                layer=resolved.get("layer", "STRUCTURAL"),
                status="RESOLVED",
                confidence=resolved["confidence"],
                provenance=semantic_data.get("provenance", "UNKNOWN"),
                framework_hint=semantic_data.get("framework_hint", ""),
                semantic_owner=semantic_data.get("resolved_owner", ""),
                metadata=self._build_metadata(chunk, resolved),
            )

            self.identity_registry.register(rel)

            relationships.append(rel)

        return relationships

    # =========================================================
    # METADATA
    # =========================================================

    def _build_metadata(self, chunk, inference):

        return {
            "chunk_id": self._chunk_id(chunk),
            "file": self._chunk_file(chunk),
            "semantic_resolution": bool(inference),
            "inference": inference or {},
        }

    # =========================================================
    # SEMANTIC CONTEXT
    # =========================================================

    def _build_semantic_context(self, chunk):

        context = SemanticContextV2()

        metadata = self._chunk_metadata(chunk)

        for assignment in metadata.get("assignments", []):

            state = AssignmentResolverV2().resolve(assignment)

            if state:
                context.set(state)

        return context

    # =========================================================
    # CHUNK HELPERS
    # =========================================================

    def _chunk_metadata(self, chunk):

        if isinstance(chunk, dict):
            return chunk.get("metadata", {})

        return getattr(chunk, "metadata", {})

    def _chunk_raw_calls(self, chunk):

        if isinstance(chunk, dict):

            metadata = chunk.get("metadata", {})

            return chunk.get("raw_calls") or metadata.get("calls") or []

        return getattr(chunk, "raw_calls", None) or getattr(chunk, "calls", [])

    def _chunk_id(self, chunk):

        if isinstance(chunk, dict):

            metadata = chunk.get("metadata", {})

            return (
                chunk.get("id")
                or metadata.get("chunk_id")
                or metadata.get("symbol_path")
            )

        return getattr(chunk, "id", None)

    def _chunk_file(self, chunk):

        if isinstance(chunk, dict):

            metadata = chunk.get("metadata", {})

            return chunk.get("file") or metadata.get("file")

        return getattr(chunk, "file", None)

    # =========================================================
    # EDGE FILTERING
    # =========================================================

    def _ensure_identity_node(self, node_id: str, mode: IdentityMode):
        """
        Controlled identity creation:
        - STRICT: do nothing (must already exist)
        - INFERRED: register lightweight semantic node
        - EXTERNAL: register external placeholder
        """

        if self.identity_registry.exists(node_id):
            return

        if mode == IdentityMode.STRICT:
            return

        node_type = "inferred" if mode == IdentityMode.INFERRED else "external"

        self.identity_registry.register(
            GraphNodeV2(
                id=node_id,
                type=node_type,
                name=node_id,
                canonical=node_id,
                metadata={"mode": mode.value},
            )
        )
