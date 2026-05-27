# pipeline_v2/core/reader/graph_reader_engine.py

from pipeline_v2.core.graph.graph_types import (
    GraphNodeV2,
    GraphEdgeV2,
)


class GraphReaderEngineV1:

    def __init__(
        self,
        repository,
        runtime_graph,
    ):

        self.repository = repository
        self.runtime = runtime_graph

    # =====================================================
    # PUBLIC
    # =====================================================

    def load_all(self):

        self.load_symbols()
        self.load_relationships()

    # =====================================================
    # SYMBOLS
    # =====================================================

    def load_symbols(self):

        rows = self.repository.fetch_all("""
            SELECT
                symbol_id,
                symbol_type,
                name,
                canonical_name,
                module_name,
                file_path,
                semantic_type
            FROM graph_v1.symbols
            """)

        for row in rows:

            node = GraphNodeV2(
                id=row[0],
                type=row[1],
                name=row[2],
                canonical=row[3],
                metadata={
                    "module_name": row[4],
                    "file_path": row[5],
                    "semantic_type": row[6],
                },
            )

            self.runtime.add_node(node)

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    def load_relationships(self):

        rows = self.repository.fetch_all("""
            SELECT
                relationship_id,
                source_symbol_id,
                target_symbol_id,
                relationship_type,
                layer,
                resolution_status,
                confidence,
                metadata
            FROM graph_v1.relationships
            """)

        for row in rows:

            edge = GraphEdgeV2(
                id=row[0],
                source=row[1],
                target=row[2],
                type=row[3],
                layer=row[4],
                status=row[5],
                confidence=float(row[6]),
                metadata=(row[7] or {}),
            )

            self.runtime.add_edge(edge)
