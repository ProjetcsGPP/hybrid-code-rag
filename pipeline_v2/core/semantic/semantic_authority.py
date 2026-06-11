# pipeline_v2/core/semantic/semantic_authority.py


from pipeline_v2.core.state.variable_state import VariableState
from pipeline_v2.core.contract.semantic_inference_result import SemanticInferenceResult
from pipeline_v2.core.contract.semantic_decision_result import (
    SemanticDecisionResult,
)


class SemanticAuthority:

    def decide(
        self,
        state: VariableState,
        inference: SemanticInferenceResult | None,
    ) -> SemanticDecisionResult:

        # =========================================================
        # BASE CANÔNICA = STATE
        # =========================================================
        semantic_type = state.semantic_type
        model = state.model
        confidence = state.confidence

        dispatch = "DIRECT"

        # =========================================================
        # OVERLAY INFERENCE (SEM MUTAR STATE)
        # =========================================================
        if inference:

            inferred_type = self._extract_relationship_type(inference)

            semantic_type = self._merge_type(
                semantic_type,
                inferred_type,
            )

            confidence = min(
                max(confidence, inference.confidence),
                0.99,
            )

            dispatch = inference.dispatch or dispatch

        # =========================================================
        # FINAL DECISION (IMUTÁVEL)
        # =========================================================
        return SemanticDecisionResult(
            variable=state.name,
            semantic_type=semantic_type,
            model=model,
            confidence=confidence,
            dispatch=dispatch,
            provenance="SEMANTIC_AUTHORITY_V2",
        )

    # =========================================================
    # SAFE EXTRACTION (EVITA DEPENDÊNCIA DE ENUM OU STRING FRÁGIL)
    # =========================================================
    def _extract_relationship_type(self, inference: SemanticInferenceResult) -> str:

        rel = inference.relationship_type

        # suporta enum ou string
        if hasattr(rel, "value"):
            return rel.value

        return str(rel)

    # =========================================================
    # MERGE RULE (CONTROLLED CONFLICT)
    # =========================================================
    def _merge_type(self, base: str, inferred: str) -> str:

        if base == "unknown":
            return inferred

        if base == inferred:
            return base

        return f"{base}|{inferred}"
