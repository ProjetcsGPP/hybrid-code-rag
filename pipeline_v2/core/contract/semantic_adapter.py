# pipeline_v2/core/contract/semantic_adapter.py

from .semantic_contract import ChunkContract
from .symbol_adapter import SymbolAdapter


class SemanticAdapter:

    # -------------------------
    # CHUNK
    # -------------------------
    @staticmethod
    def normalize_chunk(chunk: dict) -> ChunkContract:
        meta = chunk.get("metadata", {})

        return ChunkContract(
            id=meta.get("chunk_id"),
            file=meta.get("file"),
            name=meta.get("name"),
            type=meta.get("type"),
            raw_calls=meta.get("calls", []),
            metadata=meta,
        )

    # -------------------------
    # SYMBOL AST → CONTRACT
    # -------------------------
    @staticmethod
    def normalize_symbol_dict(meta: dict):
        return SymbolAdapter.from_ast(meta)
