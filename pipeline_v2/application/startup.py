# pipeline_v2/application/startup.py

from pipeline_v2.application.bootstrap_runtime import (
    build_postgres_repository,
)

from pipeline_v2.core.graph.runtime_graph import (
    graph_runtime,
)

from pipeline_v2.core.reader.graph_reader_engine import (
    GraphReaderEngineV1,
)


def preload_graph():

    repository = build_postgres_repository()

    reader = GraphReaderEngineV1(
        repository=repository,
        runtime_graph=graph_runtime,
    )

    reader.load_all()

    print(
        f"GRAPH PRELOADED | "
        f"NODES={len(graph_runtime.nodes)} | "
        f"EDGES={len(graph_runtime.edges)}"
    )
