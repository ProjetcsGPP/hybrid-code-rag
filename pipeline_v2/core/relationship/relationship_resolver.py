# pipeline_v2/core/relationship/relationship_resolver.py


from .relationship_types import RelationshipType


class RelationshipResolverV2:
    """
    V2: Relationship Resolver evoluído para Semantic Graph Engine.
    Mantém compatibilidade com pipeline antigo, mas adiciona camadas semânticas.
    """

    def resolve_call(
        self,
        caller_symbol,
        raw_call: str,
        semantic_context=None,
    ):
        """
        Entry point compatível com V1 + extensão V2.
        """

        rel_type, dispatch = self._classify(raw_call)

        semantic_data = self._resolve_semantic_owner(
            raw_call,
            semantic_context,
        )

        normalized_call = self._normalize_call(raw_call, semantic_data)

        confidence = self._calculate_confidence(
            rel_type,
            semantic_data,
        )

        return {
            # compat V1
            "relationship_type": rel_type,
            "dispatch": dispatch,
            "semantic": semantic_data,
            # V2 extension
            "layer": self._resolve_layer(rel_type, semantic_data),
            "normalized_call": normalized_call,
            "confidence": confidence,
            "resolution_path": self._build_resolution_path(rel_type, semantic_data),
        }

    # =====================================================
    # CLASSIFICATION (mantido + leve refinamento)
    # =====================================================

    def _classify(self, raw_call: str):

        if raw_call.startswith("self."):
            return RelationshipType.SELF_CALL, "SELF"

        if raw_call.startswith("super."):
            return RelationshipType.SUPER_CALL, "SUPER"

        if "objects." in raw_call:
            return RelationshipType.ORM_QUERY, "ORM"

        if "." in raw_call:
            return RelationshipType.FRAMEWORK_CALL, "FRAMEWORK"

        return RelationshipType.CALLS, "DIRECT"

    # =====================================================
    # SEMANTIC RESOLUTION (melhorado mas compatível)
    # =====================================================

    def _resolve_semantic_owner(
        self,
        raw_call: str,
        semantic_context=None,
    ):

        if not semantic_context:
            return {}

        if "." not in raw_call:
            return {}

        owner, method = raw_call.split(".", 1)

        state = semantic_context.get(owner)

        if not state:
            return {}

        resolved_symbol = state.inferred_symbol or state.model or state.source

        resolved_call = f"{resolved_symbol}.{method}" if resolved_symbol else raw_call

        return {
            "resolved_owner": state.source,
            "semantic_type": state.semantic_type,
            "model": state.model,
            "inferred_symbol": state.inferred_symbol,
            "framework_hint": state.framework_hint,
            "confidence": state.confidence,
            "provenance": state.provenance,
            "resolved_call": resolved_call,
            "metadata": state.metadata,
        }

    # =====================================================
    # V2: NORMALIZATION LAYER
    # =====================================================

    def _normalize_call(self, raw_call: str, semantic_data: dict):

        if not semantic_data:
            return raw_call

        return semantic_data.get("resolved_call", raw_call)

    # =====================================================
    # V2: LAYER RESOLUTION
    # =====================================================

    def _resolve_layer(self, rel_type, semantic_data: dict):

        if semantic_data.get("confidence", 0) > 0.85:
            return "SEMANTIC_RESOLVED"

        if rel_type == RelationshipType.ORM_QUERY:
            return "FRAMEWORK_SEMANTIC"

        if rel_type in (
            RelationshipType.SELF_CALL,
            RelationshipType.SUPER_CALL,
        ):
            return "STRUCTURAL_SEMANTIC"

        return "STRUCTURAL"

    # =====================================================
    # V2: CONFIDENCE ENGINE
    # =====================================================

    def _calculate_confidence(self, rel_type, semantic_data: dict):

        base = 0.5

        if rel_type == RelationshipType.SELF_CALL:
            base = 0.95
        elif rel_type == RelationshipType.SUPER_CALL:
            base = 0.9
        elif rel_type == RelationshipType.ORM_QUERY:
            base = 0.8

        semantic_boost = semantic_data.get("confidence", 0.0)

        return min(1.0, base * 0.7 + semantic_boost * 0.3)

    # =====================================================
    # V2: RESOLUTION TRACE
    # =====================================================

    def _build_resolution_path(self, rel_type, semantic_data: dict):

        path = ["AST_PASS"]

        if semantic_data:
            path.append("SEMANTIC_PASS")

        if rel_type == RelationshipType.ORM_QUERY:
            path.append("FRAMEWORK_PASS")

        return " -> ".join(path)
