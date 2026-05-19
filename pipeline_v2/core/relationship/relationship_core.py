from .relationship_factory import RelationshipFactoryV2
from .relationship_types import RelationshipType
from .relationship_resolver import RelationshipResolverV2

# from pipeline_v2.core.contract.semantic_adapter import SemanticAdapter
from pipeline_v2.core.contract.semantic_classifier import SemanticCallClassifier
from pipeline_v2.core.contract.semantic_contract import RelationshipContract
from pipeline_v2.core.contract.contract_enforcer import ContractEnforcer


class RelationshipCoreV2:

    def __init__(self, symbol_core=None, graph_core=None):
        self.edges = {}
        self.resolver = RelationshipResolverV2()
        self.symbol_core = symbol_core
        self.graph_core = graph_core

    def add_call(self, source, target, raw_call: str):

        rel_type, dispatch = self.resolver.resolve_call(source, raw_call)

        rel = RelationshipFactoryV2.create(
            source=source,
            target=target,
            type=rel_type,
            layer="SEMANTIC",
            status="RESOLVED",
            confidence=1.0,
            metadata={
                "dispatch": dispatch,
                "raw_call": raw_call,
            },
        )

        self.edges[rel.id] = rel
        return rel

    def add_import(self, source, target):
        rel = RelationshipFactoryV2.create(
            source=source,
            target=target,
            type=RelationshipType.IMPORT_RESOLUTION,
            layer="SEMANTIC",
        )

        self.edges[rel.id] = rel
        return rel

    def add_belongs_to(self, source, target):
        rel = RelationshipFactoryV2.create(
            source=source,
            target=target,
            type=RelationshipType.ATTRIBUTE_CALL,
            layer="STRUCTURAL",
        )

        self.edges[rel.id] = rel
        return rel

    def get_by_source(self, source: str):
        return [e for e in self.edges.values() if e.source == source]

    def _resolve_source_symbol(self, chunk, symbol_table):

        # ASTChunker returns dict
        if isinstance(chunk, dict):
            return chunk["metadata"].get("chunk_id") or chunk["metadata"].get(
                "symbol_path"
            )

        # fallback legacy
        return getattr(chunk, "id", None) or str(chunk)

    def _resolve_target_symbol(self, call, symbol_table):
        return symbol_table.get(call, call)

    def _resolve_target(self, raw_call: str, symbol_table: dict):

        # 1. local chunk resolution
        if raw_call in symbol_table:
            return symbol_table[raw_call]

        # 2. SymbolCoreV2 global index
        if self.symbol_core:
            symbol = self.symbol_core.find_by_name(raw_call)
            if symbol:
                return symbol.id

        # 3. graph runtime lookup (se tiver implementado)
        if self.graph_core:
            node = self.graph_core.get_node_by_name(raw_call)
            if node:
                return node.id

        # 4. fallback controlado
        return f"UNRESOLVED::{raw_call}"

    def process_chunk(self, chunk, symbol_table):
        """
        VERSÃO CONTRATUAL ESTABILIZADA (SEM DUPLICIDADE)
        """

        relationships = []

        # normalize chunk (OBRIGATÓRIO)
        # chunk = SemanticAdapter.normalize_chunk(chunk)
        chunk = ContractEnforcer.enforce_chunk(chunk)

        for call in chunk.raw_calls:

            source = self._resolve_source_symbol(chunk, symbol_table)
            target = self._resolve_target_symbol(call, symbol_table)

            rel_type, dispatch = SemanticCallClassifier.classify(call)

            rel = RelationshipContract(
                id=f"{rel_type}::{source}::{target}::{hash(call)}",
                source=source,
                target=target,
                type=rel_type,
                dispatch=dispatch,
                raw_call=call,
                metadata={
                    "chunk_id": chunk.id,
                    "file": chunk.file,
                },
            )

            # 🔥 agora usamos o CONTRACT (não add_call)
            self.edges[rel.id] = rel
            relationships.append(rel)

        return relationships
