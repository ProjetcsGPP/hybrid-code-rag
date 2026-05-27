# pipeline_v2/core/semantic/engine/semantic_core_engine_v2.py

from typing import Dict, Any

from pipeline_v2.core.symbol.symbol_resolver import SymbolResolverV2
from pipeline_v2.core.semantic.inheritance.inheritance_resolver_v2 import (
    InheritanceResolverV2,
)


class SemanticCoreEngineV2:
    """
    Motor semântico central do Graph V2.

    Responsável por transformar grafo estrutural em grafo semanticamente consistente.
    """

    def __init__(self, symbol_index=None, runtime_graph=None):

        self.symbol_index = symbol_index
        self.runtime_graph = runtime_graph

        self.symbol_resolver = SymbolResolverV2(symbol_index)
        self.inheritance_resolver = InheritanceResolverV2(symbol_index)

    # ----------------------------
    # ENTRY POINT
    # ----------------------------

    def process(self, graph_state: Dict[str, Any]) -> Dict[str, Any]:

        symbols = graph_state.get("symbols", [])
        relationships = graph_state.get("relationships", [])
        inheritance = graph_state.get("inheritance", [])

        # 1. Resolve symbols
        resolved_symbols = self.symbol_resolver.resolve(symbols)

        # 2. Resolve inheritance
        resolved_inheritance = self.inheritance_resolver.resolve(inheritance)

        # 3. (placeholder) relationships enrichment virá depois
        enriched_relationships = relationships

        return {
            "symbols": resolved_symbols,
            "relationships": enriched_relationships,
            "inheritance": resolved_inheritance,
        }
