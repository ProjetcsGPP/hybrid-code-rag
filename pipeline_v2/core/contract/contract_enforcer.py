# pipeline_v2/core/contract/contract_enforcer.py

from typing import Any
from .semantic_contract import ChunkContract
from pipeline_v2.core.relationship.relationship_models import (
    RelationshipV2,
)
from pipeline_v2.core.symbol.symbol_models import SymbolV2

from pipeline_v2.core.contract.graph_contracts import AssignmentContractV2


class ContractViolation(Exception):
    pass


class ContractEnforcer:

    @staticmethod
    def enforce_identity(value: Any):
        if value is None or value == "":
            raise ContractViolation("Invalid identity")
        return str(value)

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
    def enforce_symbol(symbol: Any) -> SymbolV2:
        if not isinstance(symbol, SymbolV2):
            raise ContractViolation(
                f"Symbol inválido. Esperado SymbolV2, recebido: {type(symbol)}"
            )
        return symbol

    # -------------------------
    # RELATIONSHIP
    # -------------------------
    @staticmethod
    def enforce_relationship(rel: Any) -> RelationshipV2:
        if not isinstance(rel, RelationshipV2):
            raise ContractViolation(
                f"Relationship inválido. Esperado RelationshipV2, "
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

    # -------------------------
    # ASSIGNMENT
    # -------------------------
    @staticmethod
    def enforce_assignment(assignment: Any) -> AssignmentContractV2:
        from pipeline_v2.core.contract.graph_contracts import AssignmentContractV2

        if isinstance(assignment, AssignmentContractV2):
            return assignment

        if isinstance(assignment, dict):
            return AssignmentContractV2(**assignment)

        raise ContractViolation(
            f"Assignment inválido. Esperado AssignmentContractV2 ou dict, "
            f"recebido: {type(assignment)}"
        )

    @staticmethod
    def enforce_assignments(items: list) -> list:
        return [ContractEnforcer.enforce_assignment(i) for i in items]
