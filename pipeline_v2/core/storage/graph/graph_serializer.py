# pipeline_v2/core/storage/graph/graph_serializer.py

from ...graph.graph_types import GraphNodeV2, GraphEdgeV2
from .graph_schema import NodeRecordV2, EdgeRecordV2


class GraphSerializerV2:

    # -------------------------
    # NODE
    # -------------------------
    def node_to_record(self, node: GraphNodeV2):
        return NodeRecordV2(
            id=node.id,
            type=node.type,
            name=node.name,
            canonical=node.canonical,
            metadata=node.metadata,
        )

    def record_to_node(self, record: NodeRecordV2):
        return GraphNodeV2(
            id=record.id,
            type=record.type,
            name=record.name,
            canonical=record.canonical,
            metadata=record.metadata,
        )

    # -------------------------
    # EDGE
    # -------------------------
    def edge_to_record(self, edge: GraphEdgeV2):
        return EdgeRecordV2(
            id=edge.id,
            source=edge.source,
            target=edge.target,
            type=edge.type,
            layer=edge.layer,
            status=edge.status,
            confidence=edge.confidence,
            metadata=edge.metadata,
        )

    def record_to_edge(self, record: EdgeRecordV2):
        return GraphEdgeV2(
            id=record.id,
            source=record.source,
            target=record.target,
            type=record.type,
            layer=record.layer,
            status=record.status,
            confidence=record.confidence,
            metadata=record.metadata,
        )
