# pipeline_v2/core/contract/semantic_adapter.py

from .semantic_contract import ChunkContract
from .symbol_adapter import SymbolAdapter

from .contract_enforcer import ContractEnforcer

from pipeline_v2.core.contract.graph_contracts import AssignmentContractV2


class SemanticAdapter:

    # -------------------------
    # CHUNK
    # -------------------------
    @staticmethod
    def normalize_chunk(chunk) -> ChunkContract:

        if isinstance(chunk, ChunkContract):
            return ContractEnforcer.enforce_chunk(chunk)

        meta = chunk["metadata"]

        assignments = [
            (
                AssignmentContractV2(
                    variable=a.get("variable"),
                    source=a.get("source", ""),
                    semantic_type=a.get("semantic_type", "unknown"),
                    model=a.get("model"),
                    confidence=a.get("confidence", 0.5),
                    framework_hint=a.get("framework_hint"),
                )
                if isinstance(a, dict)
                else a
            )
            for a in meta.get("assignments", [])
        ]

        chunk_contract = ChunkContract(
            id=meta["chunk_id"],
            file=meta["file"],
            name=meta["name"],
            type=meta["type"],
            raw_calls=meta["calls"] if "calls" in meta else [],
            assignments=assignments,
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
