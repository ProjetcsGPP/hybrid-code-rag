# pipeline_v2/core/state/inference_contract_guard.py

from pipeline_v2.core.state.variable_state import VariableState


class InferenceContractGuard:
    """
    Guarda de consistência para entrada do SemanticInferenceEngineV2.

    NÃO altera pipeline.
    NÃO executa inferência.
    Apenas protege contratos antes do uso.
    """

    def sanitize(self, state: VariableState) -> VariableState:

        if not isinstance(state, VariableState):
            raise TypeError(f"Invalid state: {type(state)}")

        # =========================================================
        # NORMALIZAÇÃO BÁSICA
        # =========================================================
        state.semantic_type = state.semantic_type or "unknown"
        state.source = state.source or ""
        state.model = state.model or None
        state.inferred_symbol = state.inferred_symbol or None

        # =========================================================
        # BLOQUEIO DE ATTRIBUTE CHAIN INVÁLIDO
        # =========================================================
        if state.semantic_type == "attribute_chain" and "." not in (state.source or ""):
            state.semantic_type = "unknown"

        # =========================================================
        # CONSISTÊNCIA ORM vs INSTANCE
        # =========================================================
        if state.semantic_type == "queryset" and not state.model:
            state.semantic_type = "unknown"

        if state.semantic_type == "instance" and not state.model:
            state.model = state.source

        return state
