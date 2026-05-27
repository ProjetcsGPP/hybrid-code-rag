# pipeline_v2/application/pipeline_bridge.py

from typing import List, Dict, Any

from pipeline.ast_chunker import ASTChunker

from pipeline_v2.core.symbol.symbol_core import SymbolCoreV2
from pipeline_v2.core.relationship.relationship_core import RelationshipCoreV2

from pipeline_v2.core.builder.graph_builder import GraphBuilderV2
from pipeline_v2.core.builder.build_context import BuildContextV2

from pipeline_v2.core.graph.graph_storage import GraphStorageV2

from pipeline_v2.core.normalization.graph_normalizer_v2 import GraphNormalizerV2

# from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2

from pipeline_v2.application.bootstrap_runtime import (
    identity_registry,
)

from pipeline_v2.core.identity.identity_gateway import IdentityGatewayV2
from pipeline_v2.core.semantic.semantic_graph_stabilizer_v2 import (
    SemanticGraphStabilizerV2,
)


class PipelineBridgeV2:
    """
    Pipeline oficial do CODE-RAG V2.

    Agora com:
    - Stabilization Pass (Registry + Normalizer)
    - Fase A fechada estruturalmente
    - Pronto para Fase B (Semantic Index Layer)
    """

    def __init__(self):

        self.symbol_core = SymbolCoreV2(
            identity_registry=identity_registry,
        )

        self.identity_registry = identity_registry
        self.identity = IdentityGatewayV2(identity_registry)

        self.relationship_core = RelationshipCoreV2(
            identity_registry=identity_registry,
        )

        self.graph_builder = GraphBuilderV2()
        self.storage = GraphStorageV2()

        # ❌ REMOVER registry duplicado
        # self.registry = GlobalSymbolRegistry()

        self.normalizer = GraphNormalizerV2(self.identity_registry)

        self.stabilizer = SemanticGraphStabilizerV2()

        # =========================
        # FUTURO: ENGINES
        # =========================
        self.core_engine = None
        self.experimental_engine = None

        self.trace: List[Dict[str, Any]] = []

    # =====================================================
    # INGESTION PIPELINE
    # =====================================================

    def run(self, file_path: str) -> Dict[str, Any]:

        self._log("PIPELINE_START", {"file": file_path})

        chunks = self._step_ast(file_path)
        symbols = self._step_symbols(chunks)

        # relationships = self._step_relationships(chunks, symbols)
        raw_relationships = self._step_relationships(chunks, symbols)

        relationships = self.stabilizer.stabilize(raw_relationships)

        graph_state = self._step_graph(symbols, relationships)

        # 🔴 FINAL STABILIZATION PASS (CRÍTICO)
        normalized = self._step_normalization(graph_state)

        result = self._step_storage(normalized)

        self._log("PIPELINE_END", result)

        return {"result": result, "trace": self.trace}

    # =====================================================
    # STEP 1 - AST
    # =====================================================

    def _step_ast(self, file_path: str):
        self._log("AST_CHUNKING_START", {"file": file_path})

        chunks = ASTChunker(file_path).chunk()

        self._log("AST_CHUNKING_END", {"chunks": len(chunks)})

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

            # 🔴 REGISTER GLOBAL (SOURCE OF TRUTH)
            self.identity.register_symbol(symbol)

            symbols.append(symbol)

        self._log("SYMBOL_EXTRACTION_END", {"symbols": len(symbols)})

        return symbols

    # =====================================================
    # STEP 3 - RELATIONSHIPS
    # =====================================================

    def _step_relationships(self, chunks, symbols):

        self._log("RELATIONSHIP_EXTRACTION_START", {})

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
            {"relationships": len(relationships)},
        )

        return relationships

    # =====================================================
    # STEP 4 - GRAPH BUILD
    # =====================================================

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

    # =====================================================
    # 🔴 STEP 5 - STABILIZATION PASS (NOVO)
    # =====================================================

    def _step_normalization(self, graph_state):

        self._log("NORMALIZATION_START", {})

        normalized = self.normalizer.normalize(
            nodes=graph_state["nodes_created"],
            edges=graph_state["edges_created"],
        )

        self._log(
            "NORMALIZATION_END",
            {
                "nodes": len(normalized["nodes"]),
                "edges": len(normalized["edges"]),
            },
        )

        return normalized

    # =====================================================
    # STEP 6 - STORAGE
    # =====================================================

    def _step_storage(self, normalized_graph):

        self._log("GRAPH_STORAGE_START", {})

        storage_map = {
            "nodes": len(normalized_graph["nodes"]),
            "edges": len(normalized_graph["edges"]),
        }

        # (hook futuro: persistência real estruturada)
        # self.storage.save_graph(normalized_graph)

        self._log("GRAPH_STORAGE_END", storage_map)

        return storage_map

    # =====================================================
    # ENGINE ENTRYPOINTS (FUTURO)
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

    def _log(self, stage: str, data: Dict[str, Any]):
        self.trace.append({"stage": stage, "data": data})
