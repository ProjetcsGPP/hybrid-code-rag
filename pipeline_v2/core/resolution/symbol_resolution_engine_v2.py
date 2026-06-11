# pipeline_v2/core/resolution/symbol_resolution_engine_v2.py

from typing import Dict, Any

from pipeline_v2.core.identity.resolution_workflow_v2 import (
    ResolutionEventV2,
    ResolutionEventTypeV2,
)


class SymbolResolutionEngineV2:
    """
    Autoridade central de resolução simbólica.

    Responsável por:
    - source resolution
    - target resolution
    - semantic normalization
    - unresolved fallback
    - canonical identity enforcement
    """

    def __init__(
        self,
        symbol_core=None,
        graph_core=None,
        identity_registry=None,
    ):

        self.symbol_core = symbol_core
        self.graph_core = graph_core
        self.identity_registry = identity_registry

    # =====================================================
    # NORMALIZATION
    # =====================================================

    def normalize_call(self, raw_call):

        if isinstance(raw_call, dict):

            return {
                "raw": raw_call.get("raw") or "",
                "symbol": raw_call.get("symbol"),
                "module": raw_call.get("module"),
            }

        if not isinstance(raw_call, str):

            return {
                "raw": "",
                "symbol": None,
                "module": None,
            }

        if "." in raw_call:

            parts = raw_call.split(".")

            return {
                "raw": raw_call,
                "module": ".".join(parts[:-1]),
                "symbol": parts[-1],
            }

        return {
            "raw": raw_call,
            "module": None,
            "symbol": raw_call,
        }

    # =====================================================
    # SOURCE RESOLUTION
    # =====================================================

    def resolve_source(
        self,
        chunk,
        symbol_table,
        chunk_id_fn,
        chunk_meta_fn,
    ):

        metadata = chunk_meta_fn(chunk)

        symbol_path = metadata.get("symbol_path")

        if symbol_path and symbol_path in symbol_table:

            symbol = symbol_table[symbol_path]

            if isinstance(symbol, str):
                return symbol

            return getattr(symbol, "id", symbol_path)

        return chunk_id_fn(chunk)

    # =====================================================
    # TARGET RESOLUTION
    # =====================================================

    def resolve_target(
        self,
        raw_call: Any,
        symbol_table: Dict[str, Any],
    ):

        normalized = self.normalize_call(raw_call)

        call = normalized["raw"]

        if not call:
            return None

        # -------------------------------------------------
        # 1. exact canonical
        # -------------------------------------------------

        if call in symbol_table:

            sym = symbol_table[call]

            if isinstance(sym, str):
                return sym

            return getattr(sym, "id", call)

        # -------------------------------------------------
        # 2. short symbol lookup
        # -------------------------------------------------

        short_name = normalized.get("symbol")

        if short_name and short_name in symbol_table:

            sym = symbol_table[short_name]

            if isinstance(sym, str):
                return sym

            return getattr(sym, "id", short_name)

        # -------------------------------------------------
        # 3. identity registry
        # -------------------------------------------------

        if self.identity_registry:

            resolved = self.identity_registry.resolve_by_canonical(
                call
            ) or self.identity_registry.resolve_by_name(call)

            if resolved:

                if isinstance(resolved, list):
                    resolved = resolved[0]

                return getattr(resolved, "id", str(resolved))

        # -------------------------------------------------
        # 4. symbol core lookup
        # -------------------------------------------------

        if self.symbol_core:

            matches = self.symbol_core.find_by_name(
                short_name or call,
            )

            if matches:

                first = matches[0]

                if isinstance(first, str):
                    return first

                return getattr(first, "id", str(first))

        # -------------------------------------------------
        # 5. graph lookup
        # -------------------------------------------------

        if self.graph_core:

            resolver = getattr(
                self.graph_core,
                "get_node_by_name",
                None,
            )

            if resolver:

                result = resolver(short_name or call)

                if result:
                    return getattr(result, "id", str(result))

        # -------------------------------------------------
        # 6. unresolved fallback
        # -------------------------------------------------

        return self.build_unresolved(call)

    # =====================================================
    # SEMANTIC TARGET
    # =====================================================

    def resolve_semantic_target(
        self,
        semantic_data: dict,
        symbol_table: Dict[str, Any],
    ):

        if not semantic_data:
            return None

        resolved_call = semantic_data.resolved_call if semantic_data else None

        if not resolved_call:
            return None

        return self.resolve_target(
            resolved_call,
            symbol_table,
        )

    # =====================================================
    # HELPERS
    # =====================================================

    def build_unresolved(self, call: str):

        return ResolutionEventV2(
            event_type=ResolutionEventTypeV2.FAILED_RESOLUTION,
            source=call,
            target=None,
            context={"reason": "no_match"},
        )
