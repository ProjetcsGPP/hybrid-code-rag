# pipeline_v2/core/storage/graph/graph_storage_v2.py

from pipeline_v2.core.storage.postgres.postgres_connection import (
    PostgresConnection,
)

from .graph_repository_postgres import (
    GraphRepositoryPostgresV2,
)

from .graph_serializer import GraphSerializerV2


class GraphStorageV2:

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        schema: str = "migration_v2",
    ):

        connection = PostgresConnection(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )

        self.repo = GraphRepositoryPostgresV2(
            connection=connection,
            schema=schema,
        )

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
    # LOAD GRAPH
    # -------------------------

    def load_graph(self):
        pass
