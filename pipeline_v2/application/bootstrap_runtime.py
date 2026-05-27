# pipeline_v2/application/bootstrap_runtime.py

from pipeline_v2.application.config.settings import Settings
from pipeline_v2.core.storage.postgres.postgres_connection import (
    PostgresConnection,
)
from pipeline_v2.core.storage.postgres.postgres_repository import (
    PostgresRepository,
)
from pipeline_v2.core.graph.runtime_graph import graph_runtime
from pipeline_v2.core.graph.graph_types import GraphNodeV2


def bootstrap_runtime():

    node = GraphNodeV2(
        id="node_1",
        type="function",
        name="test_function",
        canonical="test.test_function",
    )

    graph_runtime.add_node(node)


def build_postgres_repository():

    conn = PostgresConnection(
        host=Settings.DB_HOST,
        port=Settings.DB_PORT,
        database=Settings.DB_NAME,
        user=Settings.DB_USER,
        password=Settings.DB_PASSWORD,
    )

    conn.execute()

    return PostgresRepository(conn)
