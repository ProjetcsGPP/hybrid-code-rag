# pipeline_v2/core/resolution/symbol_resolution_engine_v2.py

from typing import Dict, Any


class SymbolResolutionEngineV2:
    """
    Centraliza TODA resolução de identidade simbólica.
    Remove lógica do RelationshipCore.
    """

    def __init__(self, symbol_core=None, graph_core=None, identity_registry=None):
        self.symbol_core = symbol_core
        self.graph_core = graph_core
        self.identity_registry = identity_registry

    def _normalize_call(self, raw_call):

        if isinstance(raw_call, dict):
            return raw_call.get("symbol") or raw_call.get("raw") or ""

        return raw_call

    # =====================================================
    # SOURCE
    # =====================================================

    def resolve_source(self, chunk, symbol_table, chunk_id_fn, chunk_meta_fn):

        metadata = chunk_meta_fn(chunk)
        symbol_path = metadata.get("symbol_path")

        if symbol_path and symbol_path in symbol_table:
            symbol = symbol_table[symbol_path]
            return symbol.id if not isinstance(symbol, str) else symbol

        return chunk_id_fn(chunk)

    # =====================================================
    # TARGET
    # =====================================================
    def resolve_target(self, raw_call: Any, symbol_table: Dict[str, Any]):

        call = self._normalize_call(raw_call)

        if not call:
            return None

        # 1. canonical match
        if call in symbol_table:
            sym = symbol_table[call]
            return sym.id if not isinstance(sym, str) else sym

        # 2. symbol_core lookup
        if self.symbol_core:
            matches = self.symbol_core.find_by_name(call)
            if matches:
                first = matches[0]
                return first.id if not isinstance(first, str) else first

        # 3. graph lookup
        if self.graph_core:
            node = getattr(self.graph_core, "get_node_by_name", None)
            if node:
                res = node(call)
                if res:
                    return res.id

        # 4. unresolved fallback
        return f"UNRESOLVED::{call}"
