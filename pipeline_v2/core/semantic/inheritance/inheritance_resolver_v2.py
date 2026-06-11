# pipeline_v2/core/semantic/inheritance/inheritance_resolver_v2.py

from typing import List

from pipeline_v2.core.contract.graph_contracts import InheritanceEdgeV2


class InheritanceResolverV2:
    """
    Resolve relações de herança para IDs reais de símbolos.

    Objetivo:
    - Resolver base_symbol_name → symbol_id real
    - Integrar com índice global
    - Preparar edge semântico consistente
    """

    def __init__(self, symbol_index=None):
        self.symbol_index = symbol_index

    # ----------------------------
    # ENTRY POINT
    # ----------------------------

    def resolve(
        self, inheritance_edges: List[InheritanceEdgeV2]
    ) -> List[InheritanceEdgeV2]:

        resolved = []

        for edge in inheritance_edges:
            resolved.append(self._resolve_edge(edge))

        return resolved

    # ----------------------------
    # CORE LOGIC
    # ----------------------------

    def _resolve_edge(self, edge: InheritanceEdgeV2) -> InheritanceEdgeV2:

        base_name = edge.base_symbol_name

        resolved_id = self._resolve_base_symbol(base_name)

        return InheritanceEdgeV2(
            base_symbol_name=edge.base_symbol_name,
            resolved_base_symbol_id=resolved_id,
        )

    # ----------------------------
    # RESOLUTION STRATEGY
    # ----------------------------

    def _resolve_base_symbol(self, base_name: str):

        if not base_name:
            return None

        if not self.symbol_index:
            return None

        # 1. exact match
        if base_name in self.symbol_index:
            return self.symbol_index[base_name]

        # 2. try normalized
        normalized = self._normalize(base_name)
        if normalized in self.symbol_index:
            return self.symbol_index[normalized]

        # 3. fallback external resolution
        return self._fallback_external(base_name)

    # ----------------------------
    # NORMALIZATION
    # ----------------------------

    def _normalize(self, name: str) -> str:
        return name.replace(" ", "").strip()

    # ----------------------------
    # FALLBACK
    # ----------------------------

    def _fallback_external(self, name: str) -> str:
        """
        Se não resolver, trata como external dependency.
        """

        return f"external::{name}"
