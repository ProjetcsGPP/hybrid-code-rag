# pipeline_v2/core/relationship/relationship_core.py

from .relationship_factory import RelationshipFactoryV2
from .relationship_types import RelationshipType
from .relationship_resolver import RelationshipResolverV2

from pipeline_v2.core.state.semantic_context import SemanticContextV2
from pipeline_v2.core.state.assignment_resolver import AssignmentResolverV2
from pipeline_v2.core.state.semantic_inference import SemanticInferenceEngineV2

from pipeline_v2.core.resolution.symbol_resolution_engine_v2 import (
    SymbolResolutionEngineV2,
)


class RelationshipCoreV2:
    """
    CLEAN VERSION:

    Pipeline interno agora é determinístico e linear:
    1. Source Resolution
    2. Target Resolution
    3. Semantic Inference
    4. Relationship Build
    5. Identity Enforcement
    """

    def __init__(self, symbol_core=None, graph_core=None, identity_registry=None):

        self.edges = {}

        self.resolver = RelationshipResolverV2()
        self.symbol_core = symbol_core
        self.graph_core = graph_core

        self.assignment_resolver = AssignmentResolverV2()
        self.semantic_inference = SemanticInferenceEngineV2()

        self.identity_registry = identity_registry

        self.resolution_engine = SymbolResolutionEngineV2(
            symbol_core=symbol_core,
            graph_core=graph_core,
            identity_registry=identity_registry,
        )

    # =========================================================
    # PUBLIC API (SIMPLIFIED)
    # =========================================================

    def process_chunk(self, chunk, symbol_table):

        relationships = []

        semantic_context = self._build_semantic_context(chunk)

        # 1. SOURCE (single resolution point)
        source = self.resolution_engine.resolve_source(
            chunk,
            symbol_table,
            self._chunk_id(chunk),
            self._chunk_metadata(chunk),
        )

        if not source:
            return relationships

        source = self._enforce_identity(source)

        # 2. CALL LOOP
        for raw_call in self._chunk_raw_calls(chunk):

            call = self._normalize_call(raw_call)

            resolved = self.resolver.resolve_call(
                caller_symbol=source,
                raw_call=call["raw"] if isinstance(call, dict) else str(call),
                semantic_context=semantic_context,
            )

            if not resolved.get("semantic"):
                continue

            target = resolved["semantic"].get("resolved_call")
            if not target:
                continue

            rel = RelationshipFactoryV2.create(
                source=str(source),
                target=str(target),
                type=resolved["relationship_type"],
                dispatch=resolved["dispatch"],
                raw_call=call,
                layer=resolved.get("layer", "SEMANTIC"),
                status="RESOLVED",
                confidence=resolved["confidence"],
                provenance=resolved["semantic"].get("provenance", "UNKNOWN"),
                framework_hint=resolved["semantic"].get("framework_hint", ""),
                semantic_owner=resolved["semantic"].get("resolved_owner", ""),
                metadata=self._build_metadata(chunk, semantic_context, resolved),
            )

            self.identity_registry.register(rel)

            self.edges[rel.id] = rel
            relationships.append(rel)

        return relationships

    # =========================================================
    # INFERENCE NORMALIZATION (CLEAN)
    # =========================================================

    def _apply_inference(self, inference):

        if inference:
            return (
                inference["type"],
                inference["dispatch"],
                inference["confidence"],
                inference["provenance"],
                inference.get("framework_hint", ""),
                inference.get("semantic_owner", ""),
            )

        return (
            RelationshipType.CALLS,
            "DIRECT",
            0.50,
            "AST_DIRECT",
            "",
            "",
        )

    # =========================================================
    # IDENTITY ENFORCEMENT
    # =========================================================

    def _enforce_identity(self, value):

        if not value:
            return None

        if isinstance(value, str):
            return value

        if hasattr(value, "id"):
            return self.identity_registry.resolve_id(value.id) or value.id

        return str(value)

    def _is_unresolved(self, value: str) -> bool:
        return value.startswith("UNRESOLVED::")

    # =========================================================
    # METADATA
    # =========================================================

    def _build_metadata(self, chunk, semantic_context, inference):

        return {
            "chunk_id": self._chunk_id(chunk),
            "file": self._chunk_file(chunk),
            "semantic_resolution": bool(inference),
            "inference": inference or {},
        }

    # =========================================================
    # CONTEXT BUILDER
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
    # CHUNK HELPERS (UNCHANGED)
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

    def _normalize_call(self, call):

        if isinstance(call, str):

            # tenta quebrar padrão module.function
            if "." in call:
                parts = call.split(".")
                return {
                    "raw": call,
                    "module": ".".join(parts[:-1]),
                    "symbol": parts[-1],
                }

            return {"raw": call, "module": None, "symbol": call}

        return call
