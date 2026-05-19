# pipeline_v2/core/contract/contract_enforcer.py

from typing import Any
from .semantic_contract import ChunkContract, SymbolContract, RelationshipContract


class ContractViolation(Exception):
    pass


class ContractEnforcer:

    # -------------------------
    # CHUNK
    # -------------------------
    @staticmethod
    def enforce_chunk(chunk: Any) -> ChunkContract:
        if not isinstance(chunk, ChunkContract):
            raise ContractViolation(
                f"Chunk inválido. Esperado ChunkContract, recebido: {type(chunk)}"
            )
        return chunk

    # -------------------------
    # SYMBOL
    # -------------------------
    @staticmethod
    def enforce_symbol(symbol: Any) -> SymbolContract:
        if not isinstance(symbol, SymbolContract):
            raise ContractViolation(
                f"Symbol inválido. Esperado SymbolContract, recebido: {type(symbol)}"
            )
        return symbol

    # -------------------------
    # RELATIONSHIP
    # -------------------------
    @staticmethod
    def enforce_relationship(rel: Any) -> RelationshipContract:
        if not isinstance(rel, RelationshipContract):
            raise ContractViolation(
                f"Relationship inválido. Esperado RelationshipContract, "
                f"recebido: {type(rel)}"
            )
        return rel

    # -------------------------
    # LIST VALIDATION
    # -------------------------
    @staticmethod
    def enforce_list(items: list, expected_type: type):
        for i in items:
            if not isinstance(i, expected_type):
                raise ContractViolation(
                    f"Item inválido em lista. Esperado {expected_type}, "
                    f"recebido {type(i)}"
                )
        return items
