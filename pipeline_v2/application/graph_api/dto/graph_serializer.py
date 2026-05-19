# pipeline_v2/application/graph_api/dto/graph_serializer.py

from .graph_dto import NodeDTO, EdgeDTO


class GraphSerializer:

    @staticmethod
    def node(node):
        return NodeDTO(
            id=node.id,
            type=node.type,
            name=node.name,
            canonical=getattr(node, "canonical", ""),
            metadata=getattr(node, "metadata", {}),
        )

    @staticmethod
    def edge(edge):
        return EdgeDTO(
            id=edge.id,
            source=edge.source,
            target=edge.target,
            type=edge.type,
            layer=edge.layer,
            status=edge.status,
            confidence=getattr(edge, "confidence", 1.0),
            metadata=getattr(edge, "metadata", {}),
        )
