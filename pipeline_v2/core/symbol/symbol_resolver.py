# pipeline_v2/core/symbol/symbol_resolver.py


class SymbolResolverV2:
    """
    Responsável por resolução determinística
    de símbolos canônicos.

    NÃO faz:
    - inferência semântica
    - propagação
    - runtime approximation

    Apenas binding de identidade.
    """

    def __init__(self, symbol_core=None, graph_core=None):

        self.symbol_core = symbol_core
        self.graph_core = graph_core

    # =====================================================
    # PUBLIC
    # =====================================================

    def resolve(self, canonical_call: str):

        if not canonical_call:
            return None

        # -------------------------------------------------
        # 1. CANONICAL LOOKUP
        # -------------------------------------------------

        symbol = self._resolve_canonical(
            canonical_call,
        )

        if symbol:
            return {
                "target": symbol.id,
                "strategy": "CANONICAL_SYMBOL",
                "confidence": 0.99,
            }

        # -------------------------------------------------
        # 2. NAME LOOKUP
        # -------------------------------------------------

        name = canonical_call.split(".")[-1]

        symbol = self._resolve_name(name)

        if symbol:
            return {
                "target": symbol.id,
                "strategy": "NAME_SYMBOL",
                "confidence": 0.80,
            }

        # -------------------------------------------------
        # 3. RUNTIME GRAPH
        # -------------------------------------------------

        node = self._resolve_runtime(canonical_call)

        if node:
            return {
                "target": node.id,
                "strategy": "RUNTIME_GRAPH",
                "confidence": 0.70,
            }

        return None

    # =====================================================
    # INTERNALS
    # =====================================================

    def _resolve_canonical(self, canonical):

        if not self.symbol_core:
            return None

        normalized = self._normalize(canonical)

        for symbol in self.symbol_core.index.by_id.values():

            current = self._normalize(getattr(symbol, "canonical", ""))

            if current.endswith(normalized):
                return symbol

        return None

    def _resolve_name(self, name):

        if not self.symbol_core:
            return None

        matches = self.symbol_core.find_by_name(name)

        if not matches:
            return None

        if isinstance(matches, list):

            first = matches[0]

            if isinstance(first, str):
                return self.symbol_core.get_symbol(first)

            return first

        return matches

    def _resolve_runtime(self, canonical):

        if not self.graph_core:
            return None

        for node in self.graph_core.store.nodes.values():

            if getattr(node, "canonical", None) == canonical:
                return node

        return None

    def _normalize(self, value: str):

        if not value:
            return ""

        return value.lower().strip()
