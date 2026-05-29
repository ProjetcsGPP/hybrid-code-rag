# pipeline_v2/core/builder/graph_builder.py


from ..graph.graph_types import GraphNodeV2, GraphEdgeV2

from pipeline_v2.core.contract.contract_enforcer import ContractEnforcer

from pipeline_v2.core.identity.identity_service_v2 import IdentityServiceV2


class GraphBuilderV2:

    def __init__(
        self,
        identity_registry,
        graph_core,
    ):
        self.node_index = {}
        self.graph_core = graph_core
        self.identity_registry = identity_registry
        self.identity = IdentityServiceV2(identity_registry)

    # -------------------------
    # SYMBOL INGESTION
    # -------------------------
    def ingest_symbol(self, symbol):

        symbol = ContractEnforcer.enforce_symbol(symbol)

        # 1. registry é a autoridade de registro
        node = self.identity_registry.register(symbol)

        node_id = node.id

        # 2. node final do grafo usa identity registrada
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

        # 🔥 resolve via convergence layer + registry
        source = self.identity.resolve(rel.source)
        target = self.identity.resolve(rel.target)

        if source is None or target is None:
            return None

        edge = GraphEdgeV2(
            id=rel.id,
            source=str(source),
            target=str(target),
            type=(rel.type.value if hasattr(rel.type, "value") else str(rel.type)),
            layer=rel.layer,
            status=rel.status,
            confidence=getattr(rel, "confidence", 1.0),
            metadata=rel.metadata,
        )

        self.graph_core.add_edge(edge)

        # NÃO registrar relationship como identity
        # identity já foi resolvida no RelationshipCore

        # self.identity_registry.register(rel)

        return edge

    # -------------------------
    # FULL INGEST FILE
    # -------------------------
    def ingest_file(self, context):

        # ❌ node_index REMOVED COMPLETELY

        edges = []

        # 1. symbols
        for symbol in context.symbols:
            symbol = ContractEnforcer.enforce_symbol(symbol)
            self.ingest_symbol(symbol)

        # 2. relationships
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
