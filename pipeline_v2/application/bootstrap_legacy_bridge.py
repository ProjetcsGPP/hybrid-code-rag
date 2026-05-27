# pipeline_v2/application/bootstrap_legacy_bridge.py

from pipeline.structure.storage.postgres_connection import (
    PostgresConnection,
)

from pipeline.structure.storage.postgres_structural_store import (
    PostgresStructuralStore,
)


from pipeline.structure.structural_indexer import (
    StructuralIndexer,
)

from pipeline_v2.application.bootstrap_runtime import (
    build_postgres_repository,
)

from pipeline_v2.core.writer.graph_writer_engine import (
    GraphWriterEngineV1,
)


def build_legacy_indexer_with_postgres():
    # -----------------------------------------
    # NEW LEGACY POSTGRES STORE
    # -----------------------------------------

    connection = PostgresConnection(
        host="localhost",
        port=5432,
        database="code_rag",
        user="postgres",
        password="postgres",
    )

    store = PostgresStructuralStore(
        connection=connection,
        schema="migration_legacy",
    )

    # -----------------------------------------
    # POSTGRES REPOSITORY
    # -----------------------------------------

    postgres_repository = build_postgres_repository()

    # -----------------------------------------
    # GRAPH WRITER (POSTGRES)
    # -----------------------------------------

    graph_writer = GraphWriterEngineV1(
        graph_store=postgres_repository,
    )

    # -----------------------------------------
    # STRUCTURAL INDEXER
    # -----------------------------------------

    indexer = StructuralIndexer(
        store=store,
        graph_writer=graph_writer,
    )

    return indexer
