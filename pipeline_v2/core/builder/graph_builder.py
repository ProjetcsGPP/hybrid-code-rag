# pipeline_v2/core/builder/graph_builder.py

from ..graph.graph_types import GraphNodeV2, GraphEdgeV2

from pipeline_v2.core.contract.contract_enforcer import ContractEnforcer
from pipeline_v2.core.contract.graph_contracts import GraphSubgraphV2

from pipeline_v2.core.symbol.symbol_models import SymbolV2
from pipeline_v2.core.relationship.relationship_models import RelationshipV2


class GraphBuilderV2:

    def __init__(
        self,
        identity_registry,
        graph_core,
    ):
        self.node_index = {}
        self.graph_core = graph_core
        self.identity_registry = identity_registry

    # -------------------------
    # SYMBOL INGESTION
    # -------------------------
    def ingest_symbol(self, symbol):

        symbol = ContractEnforcer.enforce_symbol(symbol)

        node = self.identity_registry.register(symbol)
        node_id = node.id

        graph_node = GraphNodeV2(
            id=node_id,
            type=(
                str(symbol.type.value)
                if hasattr(symbol.type, "value")
                else str(symbol.type)
            ),
            name=symbol.name,
            canonical=symbol.canonical,
            metadata=symbol.metadata,
        )

        self.graph_core.add_node(graph_node)

        return graph_node

    # -------------------------
    # RELATIONSHIP INGESTION
    # -------------------------
    def ingest_relationship(self, rel):

        rel = ContractEnforcer.enforce_relationship(rel)

        source = str(rel.source)
        target = str(rel.target)

        if not self.graph_core.get_node(source):
            self.graph_core.add_node(
                GraphNodeV2(
                    id=source,
                    type="inferred",
                    name=source,
                    canonical=source,
                    metadata={},
                )
            )

        if not self.graph_core.get_node(target):
            self.graph_core.add_node(
                GraphNodeV2(
                    id=target,
                    type="inferred",
                    name=target,
                    canonical=target,
                    metadata={},
                )
            )

        edge = GraphEdgeV2(
            id=rel.id,
            source=source,
            target=target,
            type=(rel.type.value if hasattr(rel.type, "value") else str(rel.type)),
            layer=rel.layer,
            status=rel.status,
            confidence=getattr(rel, "confidence", 1.0),
            metadata=rel.metadata,
        )

        self.graph_core.add_edge(edge)

        return edge

    # -------------------------
    # FULL INGEST FILE
    # -------------------------
    def ingest_file(self, context):

        edges = []

        ContractEnforcer.enforce_list(context.symbols, SymbolV2)
        for symbol in context.symbols:
            symbol = ContractEnforcer.enforce_symbol(symbol)
            self.ingest_symbol(symbol)

        ContractEnforcer.enforce_list(context.relationships, RelationshipV2)
        for rel in context.relationships:
            rel = ContractEnforcer.enforce_relationship(rel)

            edge = self.ingest_relationship(rel)

            if edge:
                edges.append(edge)

        return {
            "graph": self.graph_core,
            "edges_created": len(edges),
            "nodes_created": len(self.graph_core.store.nodes),
        }

    # -------------------------
    # BUILD
    # -------------------------
    def _build_graph(self, semantic_payload):

        return GraphSubgraphV2(
            edges=semantic_payload.get("edges", []),
            nodes=[],
        )

    def build(self, semantic_payload):
        return self._build_graph(semantic_payload)
