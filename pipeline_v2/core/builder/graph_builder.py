# pipeline_v2/core/builder/graph_builder.py

from ..symbol.symbol_core import SymbolCoreV2
from ..relationship.relationship_core import RelationshipCoreV2

from ..graph.runtime_graph import graph_runtime

from ..graph.graph_types import GraphNodeV2, GraphEdgeV2

from pipeline_v2.core.contract.contract_enforcer import ContractEnforcer


class GraphBuilderV2:

    def __init__(self):

        self.node_index = {}

        self.symbol_core = SymbolCoreV2()

        self.relationship_core = RelationshipCoreV2()

        self.graph_core = graph_runtime

    # -------------------------
    # SYMBOL INGESTION
    # -------------------------
    def ingest_symbol(self, symbol):

        symbol = ContractEnforcer.enforce_symbol(symbol)

        node = GraphNodeV2(
            id=symbol.id,
            type=str(symbol.type),
            name=symbol.name,
            canonical=symbol.canonical,
            metadata=symbol.metadata,
        )

        self.graph_core.add_node(node)

        # 🔥 INDEXAÇÃO CRÍTICA
        self.node_index[symbol.id] = node.id

        return node

    # -------------------------
    # RELATIONSHIP INGESTION
    # -------------------------
    def ingest_relationship(self, rel):

        rel = ContractEnforcer.enforce_relationship(rel)

        source = self._resolve_node(rel.source)
        target = self._resolve_node(rel.target)

        # 🔥 proteção de consistência
        if source is None or target is None:
            return None

        edge = GraphEdgeV2(
            id=rel.id,
            source=source,
            target=target,
            type=rel.type,
            layer=rel.layer,
            status=rel.status,
            confidence=getattr(rel, "confidence", 1.0),
            metadata=rel.metadata,
        )

        self.graph_core.store.add_edge(edge)

        return edge

    # -------------------------
    # FULL INGEST FILE
    # -------------------------
    def ingest_file(self, context):

        # 1. RESET de estado local
        self.node_index = {}

        # 2. symbols primeiro (garante identidade)
        for symbol in context.symbols:

            symbol = ContractEnforcer.enforce_symbol(symbol)

            self.ingest_symbol(symbol)

        # 3. relationships depois (com resolução)
        edges = []
        for rel in context.relationships:

            rel = ContractEnforcer.enforce_relationship(rel)

            edge = self.ingest_relationship(rel)

            if edge:
                edges.append(edge)

        return {
            "graph": self.graph_core,
            "edges_created": len(edges),
            "nodes_created": len(self.node_index),
        }

    def _resolve_node(self, ref_id: str):
        """
        Resolve símbolo → node real do grafo
        """

        return self.node_index.get(ref_id, ref_id)
