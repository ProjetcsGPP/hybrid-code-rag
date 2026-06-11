# pipeline_v2/core/relationship/relationship_resolver.py


from .relationship_types import RelationshipType

from pipeline_v2.core.contract.relationship_resolution_result import (
    RelationshipResolutionResult,
)
from pipeline_v2.core.semantic.semantic_authority import (
    SemanticAuthority,
)

from pipeline_v2.core.contract.semantic_classifier import (
    SemanticCallClassifier,
)

from pipeline_v2.core.contract.semantic_resolution_payload import (
    SemanticResolutionPayload,
)


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

        self.semantic_authority = SemanticAuthority()

        self.semantic_classifier = SemanticCallClassifier()

        rel_type, dispatch = self.semantic_classifier.classify(raw_call)

        semantic_data = self._resolve_semantic_owner(
            raw_call,
            semantic_context,
        )

        normalized_call = self._normalize_call(raw_call, semantic_data)

        confidence = self._calculate_confidence(
            rel_type,
            semantic_data,
        )

        return RelationshipResolutionResult(
            relationship_type=rel_type,
            dispatch=dispatch,
            semantic=semantic_data,
            layer=self._resolve_layer(
                rel_type,
                semantic_data,
            ),
            normalized_call=normalized_call,
            confidence=confidence,
            resolution_path=self._build_resolution_path(
                rel_type,
                semantic_data,
            ),
        )

    # =====================================================
    # SEMANTIC RESOLUTION (melhorado mas compatível)
    # =====================================================

    def _resolve_semantic_owner(
        self,
        raw_call: str,
        semantic_context=None,
    ):

        if not semantic_context:
            return None

        if "." not in raw_call:
            return None

        owner, method = raw_call.split(".", 1)

        state = semantic_context.resolve_variable(owner)

        if not state:
            return None

        decision = self.semantic_authority.decide(state, None)

        resolved_symbol = state.inferred_symbol or decision.model or state.source

        resolved_call = f"{resolved_symbol}.{method}" if resolved_symbol else raw_call

        return SemanticResolutionPayload(
            resolved_owner=state.source,
            semantic_type=decision.semantic_type,
            model=decision.model,
            dispatch=decision.dispatch,
            inferred_symbol=state.inferred_symbol,
            framework_hint=state.framework_hint,
            confidence=decision.confidence,
            provenance=decision.provenance,
            resolved_call=resolved_call,
            metadata=state.metadata,
        )

    # =====================================================
    # V2: NORMALIZATION LAYER
    # =====================================================

    def _normalize_call(
        self,
        raw_call: str,
        semantic_data: SemanticResolutionPayload | None,
    ):

        if semantic_data is None:
            return raw_call

        return semantic_data.resolved_call or raw_call

    # =====================================================
    # V2: LAYER RESOLUTION
    # =====================================================

    def _resolve_layer(self, rel_type, semantic_data: dict):

        if semantic_data and semantic_data.confidence > 0.85:
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

        semantic_boost = semantic_data.confidence if semantic_data else 0.0

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
