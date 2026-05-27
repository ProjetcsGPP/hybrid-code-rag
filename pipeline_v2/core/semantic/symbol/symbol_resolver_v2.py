# pipeline_v2/core/semantic/symbol/symbol_resolver_v2.py

from .symbol_resolution_result import SymbolResolutionResult


class SymbolResolverV2:
    """
    Semantic Symbol Resolver.

    Responsabilidades:
    - semantic ownership resolution
    - instance propagation resolution
    - framework-aware resolution
    - canonical semantic lookup
    """

    def __init__(self, symbol_index=None):

        self.symbol_index = symbol_index

    # =====================================================
    # ENTRYPOINT
    # =====================================================

    def resolve_call(
        self,
        raw_call: str,
        semantic_state=None,
        current_symbol=None,
    ) -> SymbolResolutionResult:

        if "." not in raw_call:

            return SymbolResolutionResult(
                resolved_target=raw_call,
                confidence=0.3,
                provenance="DIRECT_CALL",
                normalized_call=raw_call,
            )

        owner, method = raw_call.split(".", 1)

        # -------------------------------------------------
        # semantic state resolution
        # -------------------------------------------------

        if semantic_state and owner in semantic_state:

            state = semantic_state[owner]

            resolved_owner = state.inferred_symbol or state.model or state.source

            normalized_call = (
                f"{resolved_owner}.{method}" if resolved_owner else raw_call
            )

            return SymbolResolutionResult(
                resolved_owner=resolved_owner,
                resolved_target=normalized_call,
                semantic_type=state.semantic_type,
                framework_hint=state.framework_hint,
                confidence=state.confidence,
                provenance=state.provenance,
                normalized_call=normalized_call,
                metadata={
                    "semantic_owner": owner,
                    "model": state.model,
                },
            )

        # -------------------------------------------------
        # fallback
        # -------------------------------------------------

        return SymbolResolutionResult(
            resolved_target=raw_call,
            confidence=0.2,
            provenance="UNRESOLVED",
            normalized_call=raw_call,
        )
