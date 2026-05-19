# pipeline_v2/core/storage/graph/graph_storage_v2.py

from .graph_repository import GraphRepositoryV2
from .graph_serializer import GraphSerializerV2


class GraphStorageV2:

    def __init__(self, db_path: str = "graph_v2.db"):
        self.repo = GraphRepositoryV2(db_path)
        self.serializer = GraphSerializerV2()

    # -------------------------
    # SAVE NODE
    # -------------------------
    def save_node(self, node):
        record = self.serializer.node_to_record(node)
        self.repo.save_node(record)

    # -------------------------
    # SAVE EDGE
    # -------------------------
    def save_edge(self, edge):
        record = self.serializer.edge_to_record(edge)
        self.repo.save_edge(record)

    # -------------------------
    # LOAD (future rebuild)
    # -------------------------
    def load_graph(self):
        # futuro: reconstrução completa do GraphCoreV2
        pass
