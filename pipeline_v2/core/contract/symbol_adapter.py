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

        required = [
            "name",
            "type",
        ]

        missing = [x for x in required if x not in meta or not meta[x]]

        if missing:
            raise ValueError(f"Invalid AST Symbol. Missing fields: {missing}")

        return SymbolContract(
            id=meta["symbol_path"] if "symbol_path" in meta else meta["chunk_id"],
            name=meta["name"],
            type=meta["type"],
            file_path=meta["file"] if "file" in meta else None,
            canonical=(
                meta["symbol_path"]
                if "symbol_path" in meta
                else f"{meta['file']}.{meta['name']}"
            ),
            parent=meta["parent_class"] if "parent_class" in meta else None,
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
