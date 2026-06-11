# pipeline_v2/core/state/semantic_inference.py


from pipeline_v2.core.relationship.relationship_types import (
    RelationshipType,
)

from pipeline_v2.core.contract.semantic_classifier import (
    SemanticCallClassifier,
)

from pipeline_v2.core.contract.semantic_inference_result import (
    SemanticInferenceResult,
)

from pipeline_v2.core.state.inference_contract_guard import (
    InferenceContractGuard,
)


class SemanticInferenceEngineV2:

    QUERYSET_METHODS = {
        "filter",
        "exclude",
        "exists",
        "first",
        "last",
        "get",
        "create",
        "update",
        "delete",
    }

    def __init__(self):
        self.guard = InferenceContractGuard()

    def resolve_call(
        self,
        raw_call: str,
        semantic_context,
    ):

        if "." not in raw_call:
            return None

        owner, method = raw_call.split(".", 1)

        state = semantic_context.resolve_variable(owner)

        if not state:
            return None

        state = self.guard.sanitize(state)

        # =====================================================
        # QUERYSET PROPAGATION
        # =====================================================

        if state.semantic_type == "queryset" and method in self.QUERYSET_METHODS:
            return self._build_queryset_result(
                state,
                method,
            )

        # =====================================================
        # INSTANCE PROPAGATION
        # =====================================================

        if state.semantic_type == "instance":
            return self._build_instance_result(
                state,
                method,
            )

        # =====================================================
        # ATTRIBUTE CHAIN PROPAGATION
        # =====================================================

        if state.semantic_type == "attribute_chain" and state.source:
            return self._build_chain_result(
                state,
                method,
            )

        return None

    # =====================================================
    # BUILDERS
    # =====================================================

    def _build_queryset_result(
        self,
        state,
        method,
    ):

        dispatch = "ORM"

        SemanticCallClassifier.validate_dispatch(dispatch)

        return SemanticInferenceResult(
            relationship_type=RelationshipType.ORM_QUERYSET_CALL,
            dispatch=dispatch,
            confidence=min(
                state.confidence + 0.03,
                0.99,
            ),
            semantic_owner=f"QuerySet<{state.model}>",
            framework_hint="django",
            provenance="QUERYSET_PROPAGATION",
            resolved_call=f"{state.model}.{method}",
            inferred_symbol=state.inferred_symbol,
        )

    def _build_instance_result(
        self,
        state,
        method,
    ):

        dispatch = "INSTANCE"

        SemanticCallClassifier.validate_dispatch(dispatch)

        return SemanticInferenceResult(
            relationship_type=RelationshipType.INSTANCE_METHOD_CALL,
            dispatch=dispatch,
            confidence=min(
                state.confidence,
                0.95,
            ),
            semantic_owner=state.model,
            framework_hint=state.framework_hint,
            provenance="INSTANCE_ASSIGNMENT_PROPAGATION",
            resolved_call=f"{state.model}.{method}",
            inferred_symbol=state.inferred_symbol,
        )

    def _build_chain_result(
        self,
        state,
        method,
    ):

        dispatch = "CHAIN"

        SemanticCallClassifier.validate_dispatch(dispatch)

        return SemanticInferenceResult(
            relationship_type=RelationshipType.CHAINED_ATTRIBUTE_CALL,
            dispatch=dispatch,
            confidence=min(
                state.confidence,
                0.90,
            ),
            semantic_owner=state.source,
            framework_hint=state.framework_hint,
            provenance="ATTRIBUTE_CHAIN_PROPAGATION",
            resolved_call=f"{state.source}.{method}",
            inferred_symbol=state.inferred_symbol,
        )
