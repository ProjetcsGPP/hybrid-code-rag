# pipeline_v2/core/contract/symbol_adapter.py

from typing import Dict, Any

from ..symbol.symbol_models import SymbolV2
from .semantic_contract import SymbolContract


class SymbolAdapter:

    # -------------------------
    # AST → CONTRACT
    # -------------------------
    @staticmethod
    def from_ast(meta: Dict[str, Any]) -> SymbolContract:
        return SymbolContract(
            id=meta.get("symbol_path") or meta.get("chunk_id"),
            name=meta.get("name"),
            type=meta.get("type"),
            file_path=meta.get("file"),
            canonical=meta.get("symbol_path")
            or f"{meta.get('file')}.{meta.get('name')}",
            parent=meta.get("parent_class"),
            metadata={
                k: v for k, v in meta.items() if k not in ["name", "type", "file"]
            },
        )

    # -------------------------
    # SYMBOLV2 → CONTRACT
    # -------------------------
    @staticmethod
    def from_factory(symbol: SymbolV2) -> SymbolContract:
        return SymbolContract(
            id=symbol.id,
            name=symbol.name,
            type=str(symbol.type),
            file_path=symbol.file_path,
            canonical=symbol.canonical,
            parent=getattr(symbol, "parent", None),
            metadata=symbol.metadata or {},
        )
