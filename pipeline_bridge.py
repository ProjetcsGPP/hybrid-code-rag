# pipeline_bridge.py


"""
LEGACY PIPELINE - NÃO USAR PARA NOVAS INGESTÕES
SUBSTITUÍDO POR pipeline_v2.application.pipeline_bridge.PipelineBridgeV2
"""

from pipeline_v2.core.symbol.symbol_resolver import (
    SymbolResolverV2,
)
from pipeline_v2.core.inheritance.inheritance_resolver import (
    InheritanceResolverV2,
)
from pipeline_v2.application.bootstrap_runtime import build_postgres_repository

from pipeline_v2.core.semantic.engine.semantic_core_engine_v2 import (
    SemanticCoreEngineV2,
)

from pipeline.ast_chunker import ASTChunker


class PipelineBridge:

    def __init__(self, mode="v2"):
        self.symbol_resolver = SymbolResolverV2()
        self.inheritance_resolver = InheritanceResolverV2()

        self.semantic_engine = SemanticCoreEngineV2(
            repository=build_postgres_repository()
        )

    def run(self, file_path: str):

        chunks = ASTChunker(file_path).chunk()

        symbols = self.symbol_resolver.resolve(chunks)

        inheritance = self.inheritance_resolver.resolve(chunks, symbols)

        result = self.semantic_engine.ingest(symbols=symbols, inheritance=inheritance)

        return result
