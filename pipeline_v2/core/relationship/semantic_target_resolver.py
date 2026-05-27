# pipeline_v2/core/relationship/semantic_target_resolver.py

from pipeline_v2.core.symbol.symbol_resolver import SymbolResolverV2


class SemanticTargetResolverV2:

    def __init__(
        self,
        symbol_core=None,
        graph_core=None,
    ):

        self.symbol_resolver = SymbolResolverV2(
            symbol_core=symbol_core,
            graph_core=graph_core,
        )

    # =====================================================
    # PUBLIC
    # =====================================================

    def resolve(
        self,
        raw_call: str,
        semantic_data: dict,
    ):

        if not semantic_data:
            return None

        resolved_call = semantic_data.get(
            "resolved_call",
        )

        if not resolved_call:
            return None

        result = self.symbol_resolver.resolve(
            resolved_call,
        )

        if not result:
            return None

        return {
            "target": result["target"],
            "resolved_call": resolved_call,
            "strategy": result["strategy"],
            "confidence": result["confidence"],
            "provenance": "TARGET_SEMANTIC_RESOLUTION",
        }
