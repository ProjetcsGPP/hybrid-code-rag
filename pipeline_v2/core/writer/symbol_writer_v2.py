# pipeline_v2/core/writer/symbol_writer_v2.py

from pipeline_v2.core.repository.scoped_symbol_repository_v2 import (
    ScopedSymbolRepositoryV2,
)


class SymbolWriterV2:

    def __init__(
        self,
        graph_store,
    ):

        self.repository = ScopedSymbolRepositoryV2(
            graph_store,
        )

    def write(
        self,
        symbol,
        scope,
    ):

        self.repository.upsert_symbol(
            symbol,
            scope,
        )
