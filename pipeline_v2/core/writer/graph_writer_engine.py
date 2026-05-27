# pipeline_v2/core/writer/graph_writer_engine_v2.py

from pipeline_v2.core.writer.symbol_writer_v2 import (
    SymbolWriterV2,
)

from pipeline_v2.core.writer.relationship_writer_v2 import (
    RelationshipWriterV2,
)

from pipeline_v2.core.writer.inheritance_writer_v2 import (
    InheritanceWriterV2,
)


class GraphWriterEngineV2:

    def __init__(
        self,
        graph_store,
    ):

        self.symbol_writer = SymbolWriterV2(
            graph_store,
        )

        self.relationship_writer = RelationshipWriterV2(
            graph_store,
        )

        self.inheritance_writer = InheritanceWriterV2(
            graph_store,
        )

    def write_symbol(
        self,
        symbol,
        scope,
    ):

        self.symbol_writer.write(
            symbol,
            scope,
        )

        self.inheritance_writer.write(
            symbol,
            scope,
        )

        for relationship in getattr(
            symbol,
            "resolved_relationships",
            [],
        ):

            self.relationship_writer.write(
                relationship,
                scope,
            )
