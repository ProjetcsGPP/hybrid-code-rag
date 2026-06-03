# pipeline_v2/core/contract/semantic_adapter.py

from .semantic_contract import ChunkContract
from .symbol_adapter import SymbolAdapter

from .contract_enforcer import ContractEnforcer


class SemanticAdapter:

    # -------------------------
    # CHUNK
    # -------------------------
    @staticmethod
    def normalize_chunk(chunk: dict) -> ChunkContract:
        meta = chunk.get("metadata", {})

        chunk_contract = ChunkContract(
            id=meta.get("chunk_id"),
            file=meta.get("file"),
            name=meta.get("name"),
            type=meta.get("type"),
            raw_calls=meta.get("calls", []),
            assignments=meta.get("assignments", []),
            metadata=meta,
        )

        return ContractEnforcer.enforce_chunk(chunk_contract)

    # -------------------------
    # SYMBOL AST → CONTRACT
    # -------------------------
    @staticmethod
    def normalize_symbol_dict(meta: dict):

        contract = SymbolAdapter.from_ast(meta)

        return contract
