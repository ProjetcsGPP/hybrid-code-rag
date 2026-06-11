# pipeline_v2/core/contract/semantic_adapter.py

from .semantic_contract import ChunkContract
from .symbol_adapter import SymbolAdapter

from .contract_enforcer import ContractEnforcer


class SemanticAdapter:

    # -------------------------
    # CHUNK
    # -------------------------
    @staticmethod
    def normalize_chunk(chunk) -> ChunkContract:

        if isinstance(chunk, ChunkContract):
            return ContractEnforcer.enforce_chunk(chunk)

        meta = chunk["metadata"]

        chunk_contract = ChunkContract(
            id=meta["chunk_id"],
            file=meta["file"],
            name=meta["name"],
            type=meta["type"],
            raw_calls=meta["calls"] if "calls" in meta else [],
            assignments=meta["assignments"] if "assignments" in meta else [],
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
