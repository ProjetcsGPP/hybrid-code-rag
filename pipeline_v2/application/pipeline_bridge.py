# pipeline_v2/application/pipeline_bridge.py

from typing import List, Dict, Any

from pipeline.ast_chunker import ASTChunker

from pipeline_v2.core.symbol.symbol_core import SymbolCoreV2
from pipeline_v2.core.relationship.relationship_core import RelationshipCoreV2

from pipeline_v2.core.builder.graph_builder import GraphBuilderV2
from pipeline_v2.core.builder.build_context import BuildContextV2

from pipeline_v2.core.semantic.semantic_graph_stabilizer_v2 import (
    SemanticGraphStabilizerV2,
)


class PipelineBridgeV2:

    # Pipeline oficial do CODE-RAG V2.

    # Agora com:
    # - runtime isolado
    # - identity scope explícito
    # - graph scope explícito
    # - deterministic execution

    def __init__(self, runtime):

        self.runtime = runtime

        self.identity_registry = runtime.identity_registry

        self.graph_runtime = runtime.graph_runtime

        self.mutation_auditor = runtime.mutation_auditor

        # =====================================================
        # CORES
        # =====================================================

        self.symbol_core = SymbolCoreV2(
            identity_registry=self.identity_registry,
        )

        self.relationship_core = RelationshipCoreV2(
            symbol_core=self.symbol_core,
            graph_core=self.graph_runtime,
            identity_registry=self.identity_registry,
        )

        self.graph_builder = GraphBuilderV2(
            identity_registry=self.identity_registry,
            graph_core=self.graph_runtime,
        )

        # =====================================================
        # STORAGE
        # =====================================================

        self.storage = None

        # =====================================================
        # STABILIZER
        # =====================================================

        self.stabilizer = SemanticGraphStabilizerV2()

        # =====================================================
        # FUTURE ENGINES
        # =====================================================

        self.core_engine = None

        self.experimental_engine = None

        # =====================================================
        # TRACE
        # =====================================================

        self.trace: List[Dict[str, Any]] = []

        # =====================================================
        # INGESTION PIPELINE
        # =====================================================

    def run(self, file_path: str) -> Dict[str, Any]:

        self._log("PIPELINE_START", {"file": file_path})

        chunks = self._step_ast(file_path)

        symbols = self._step_symbols(chunks)

        raw_relationships = self._step_relationships(
            chunks,
            symbols,
        )

        relationships = self.stabilizer.stabilize(raw_relationships)

        graph_state = self._step_graph(
            symbols,
            relationships,
        )

        result = self._step_storage(graph_state)

        self._log("PIPELINE_END", result)

        return {
            "result": result,
            "trace": self.trace,
        }

    # =====================================================
    # STEP 1 - AST
    # =====================================================

    def _step_ast(self, file_path: str):

        self._log(
            "AST_CHUNKING_START",
            {"file": file_path},
        )

        chunks = ASTChunker(file_path).chunk()

        self._log(
            "AST_CHUNKING_END",
            {"chunks": len(chunks)},
        )

        return chunks

    # =====================================================
    # STEP 2 - SYMBOLS
    # =====================================================

    def _step_symbols(self, chunks):

        self._log("SYMBOL_EXTRACTION_START", {})

        symbols = []

        for chunk in chunks:

            meta = chunk["metadata"]

            symbol = self.symbol_core.create_symbol(
                name=meta["name"],
                type=meta["type"],
                file_path=meta["file"],
                canonical=meta.get("symbol_path"),
                metadata=meta,
            )

            symbols.append(symbol)

        self._log(
            "SYMBOL_EXTRACTION_END",
            {"symbols": len(symbols)},
        )

        return symbols

    # =====================================================
    # STEP 3 - RELATIONSHIPS
    # =====================================================

    def _step_relationships(self, chunks, symbols):

        self._log(
            "RELATIONSHIP_EXTRACTION_START",
            {},
        )

        symbol_table = {s.canonical: s for s in symbols}

        relationships = []

        for chunk in chunks:

            rels = self.relationship_core.process_chunk(
                chunk,
                symbol_table,
            )

            if rels:
                relationships.extend(rels)

        self._log(
            "RELATIONSHIP_EXTRACTION_END",
            {
                "relationships": len(relationships),
            },
        )

        return relationships

    # =====================================================
    # STEP 4 - GRAPH BUILD
    # =====================================================

    def _step_graph(
        self,
        symbols,
        relationships,
    ):

        self._log("GRAPH_BUILD_START", {})

        context = BuildContextV2(
            file_path="runtime",
            symbols=symbols,
            relationships=relationships,
        )

        graph_state = self.graph_builder.ingest_file(context)

        self._log(
            "GRAPH_BUILD_END",
            {
                "nodes": graph_state["nodes_created"],
                "edges": graph_state["edges_created"],
            },
        )

        return graph_state

    # =====================================================
    # STEP 5 - STORAGE
    # =====================================================

    def _step_storage(self, graph_state):

        self._log(
            "GRAPH_STORAGE_START",
            {},
        )

        storage_map = {
            "nodes": graph_state["nodes_created"],
            "edges": graph_state["edges_created"],
        }

        self._log(
            "GRAPH_STORAGE_END",
            storage_map,
        )

        return storage_map

    # =====================================================
    # ENGINE ENTRYPOINTS
    # =====================================================

    def set_core_engine(self, engine):
        self.core_engine = engine

    def set_experimental_engine(self, engine):
        self.experimental_engine = engine

    def query(self, node_id: str):

        if not self.core_engine:
            raise Exception("Core engine not initialized")

        return self.core_engine.retrieve(node_id)

    def analyze(self, node_id: str):

        if not self.experimental_engine:
            raise Exception("Experimental engine not initialized")

        return self.experimental_engine.analyze(node_id)

    def unified(self, node_id: str):

        return {
            "core": self.query(node_id),
            "experimental": self.analyze(node_id),
        }

    # =====================================================
    # TRACE
    # =====================================================

    def _log(
        self,
        stage: str,
        data: Dict[str, Any],
    ):
        self.trace.append(
            {
                "stage": stage,
                "data": data,
            }
        )
