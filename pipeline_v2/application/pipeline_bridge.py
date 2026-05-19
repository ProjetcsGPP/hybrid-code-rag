# pipeline_v2/application/pipeline_bridge.py

from typing import List, Dict, Any

from pipeline_v2.core.symbol.symbol_core import SymbolCoreV2
from pipeline_v2.core.relationship.relationship_core import RelationshipCoreV2

from pipeline_v2.core.builder.graph_builder import GraphBuilderV2
from pipeline_v2.core.builder.build_context import BuildContextV2

from pipeline_v2.core.graph.graph_storage import GraphStorageV2
from pipeline.ast_chunker import ASTChunker


class PipelineBridgeV2:
    """
    Orquestrador principal do CODE-RAG V2.

    Responsável por transformar código-fonte em grafo semântico completo.
    """

    def __init__(self):

        self.symbol_core = SymbolCoreV2()
        self.relationship_core = RelationshipCoreV2()
        self.graph_builder = GraphBuilderV2()
        self.storage = GraphStorageV2()

        self.trace: List[Dict[str, Any]] = []

    # -------------------------
    # ENTRY POINT
    # -------------------------

    def run(self, file_path: str) -> Dict[str, Any]:
        """
        Executa pipeline completo em um arquivo.
        """

        self._log("PIPELINE_START", {"file": file_path})

        # 1. AST CHUNKING
        chunks = self._step_ast(file_path)

        # 2. SYMBOL EXTRACTION
        symbols = self._step_symbols(chunks)

        # 3. RELATIONSHIP EXTRACTION
        relationships = self._step_relationships(chunks, symbols)

        # 4. GRAPH BUILD
        graph_state = self._step_graph(symbols, relationships)

        # 5. STORAGE
        result = self._step_storage(graph_state)

        self._log("PIPELINE_END", result)

        return {"result": result, "trace": self.trace}

    # -------------------------
    # STEP 1: AST
    # -------------------------

    def _step_ast(self, file_path: str):
        self._log("AST_CHUNKING_START", {"file": file_path})

        chunker = ASTChunker(file_path)
        chunks = chunker.chunk()

        self._log("AST_CHUNKING_END", {"chunks": len(chunks)})

        return chunks

    # -------------------------
    # STEP 2: SYMBOLS
    # -------------------------

    def _step_symbols(self, chunks):

        self._log("SYMBOL_EXTRACTION_START", {})

        symbols = []

        for chunk in chunks:

            meta = chunk["metadata"]

            symbol = self.symbol_core.create_symbol(
                name=meta["name"],
                type=meta["type"],
                file_path=meta["file"],
                canonical=meta["symbol_path"],
                metadata=meta,
            )

            symbols.append(symbol)

        self._log("SYMBOL_EXTRACTION_END", {"symbols": len(symbols)})

        return symbols

    # -------------------------
    # STEP 3: RELATIONSHIPS
    # -------------------------

    def _step_relationships(self, chunks, symbols):

        self._log("RELATIONSHIP_EXTRACTION_START", {})

        symbol_table = {s.name: s for s in symbols}

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
            {"relationships": len(relationships)},
        )

        return relationships

    # -------------------------
    # STEP 4: GRAPH BUILD
    # -------------------------

    def _step_graph(self, symbols, relationships):
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

    # -------------------------
    # STEP 5: STORAGE
    # -------------------------

    def _step_storage(self, graph_state):
        self._log("GRAPH_STORAGE_START", {})

        storage_map = self._persist_graph(graph_state)

        self._log("GRAPH_STORAGE_END", storage_map)

        return storage_map

    # -------------------------
    # GRAPH PERSISTENCE
    # -------------------------

    def _persist_graph(self, graph_state):

        return {
            "nodes": graph_state["nodes_created"],
            "edges": graph_state["edges_created"],
        }

    # -------------------------
    # LOGGING / TRACE
    # -------------------------

    def _log(self, stage: str, data: Dict[str, Any]):
        self.trace.append({"stage": stage, "data": data})
