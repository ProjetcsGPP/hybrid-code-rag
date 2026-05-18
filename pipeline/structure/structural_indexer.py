# pipeline/structure/structural_indexer.py

from pipeline.structure.symbol_extractor import SymbolExtractor
from pipeline.structure.relationship_extractor import RelationshipExtractor
from pipeline.structure.storage.sqlite_store import SQLiteStructuralStore
from pipeline.structure.resolver.symbol_index import SymbolIndex
from pipeline.structure.resolver.call_resolver import CallResolver

from pipeline.structure.graph.graph_store import GraphStore
from pipeline.structure.graph.semantic_graph_builder import SemanticGraphBuilder

from pipeline.structure.semantic.semantic_reference_builder import (
    SemanticReferenceBuilder,
)

from pipeline.structure.semantic.variable_flow_builder import VariableFlowBuilder


class StructuralIndexer:

    def __init__(self, store: SQLiteStructuralStore):

        self.store = store

        self.graph_store = GraphStore(store)

        self.symbol_extractor = SymbolExtractor()

        self._symbol_index = SymbolIndex()

        self.relationship_extractor = RelationshipExtractor(self._symbol_index)

        self._resolver = CallResolver(self._symbol_index)

        self.semantic_graph_builder = SemanticGraphBuilder(
            graph_store=self.graph_store, semantic_resolver=self._resolver
        )

        self.semantic_reference_builder = SemanticReferenceBuilder()

        self._symbols_buffer = []

        self.variable_flow_builder = VariableFlowBuilder()

    # ---------------------------------------------
    # PASS 1 — SYMBOL EXTRACTION
    # ---------------------------------------------

    def index_chunks_pass1(self, chunks: list[dict]):

        self._symbols_buffer = []

        self._symbol_index = SymbolIndex()

        # -----------------------------------------
        # REBUILD DEPENDENCIES
        # -----------------------------------------

        self.relationship_extractor = RelationshipExtractor(self._symbol_index)

        self._resolver = CallResolver(self._symbol_index)

        self.semantic_graph_builder = SemanticGraphBuilder(
            graph_store=self.graph_store, semantic_resolver=self._resolver
        )

        symbols = []

        for chunk in chunks:

            meta = chunk.get("metadata", {})

            print("\nRAW CALLS:", meta.get("calls"))
            print("CHUNK:", meta.get("chunk_id"))

            symbol = self.symbol_extractor.extract(chunk)

            self.store.save_symbol(symbol)

            self._symbols_buffer.append(symbol)

            symbols.append(symbol)

            self._symbol_index.add(symbol)

            print("CANONICAL:", symbol.canonical_name)
            print("IMPORTS:", symbol.imports)

        return symbols

    # ---------------------------------------------
    # PASS 2 — RELATIONSHIPS
    # ---------------------------------------------
    def index_chunks_pass2(self):

        relationships = []

        semantic_references = []

        for symbol in self._symbols_buffer:

            print("\nINDEX_CHUNKS_PASS2")

            print("\nINDEXING RELATIONSHIPS FOR SYMBOL:", symbol.symbol_id)

            print("\nSTRUCTURAL INDEXER")

            print("INDEX ID:", id(self._symbol_index))

            # -------------------------------------
            # HIERARCHY RELATIONSHIPS
            # -------------------------------------

            rels = self.relationship_extractor.extract(
                symbol,
                self._symbol_index,
                self._resolver,
            )

            for r in rels:

                self.store.save_relationship(r)

                relationships.append(r)

            # -------------------------------------
            # VARIABLE FLOW
            # -------------------------------------

            variable_registry = self.variable_flow_builder.build_registry(symbol)

            # -------------------------------------
            # SEMANTIC CALL EDGES
            # -------------------------------------

            call_edges = self.semantic_graph_builder.build_edges(
                symbol, variable_registry
            )

            for edge in call_edges:

                self.graph_store.save_edge(edge)

                relationships.append(edge)

            # -------------------------------------
            # SEMANTIC REFERENCES
            # -------------------------------------

            refs = self.semantic_reference_builder.build(
                symbol=symbol,
                symbol_index=self._symbol_index,
                variable_registry=variable_registry,
            )

            for ref in refs:

                self.store.save_semantic_reference(ref)

                semantic_references.append(ref)

        return relationships, semantic_references

    # ---------------------------------------------
    # PIPELINE ORCHESTRATOR
    # ---------------------------------------------

    def index_chunks(self, chunks: list[dict]):

        symbols = self.index_chunks_pass1(chunks)

        (
            relationships,
            semantic_references,
        ) = self.index_chunks_pass2()

        graph_stats = self.store.get_graph_stats()

        print("\nGRAPH SUMMARY:")

        print("NODES:", graph_stats["nodes"])

        print("EDGES:", graph_stats["edges"])

        print(
            "REFERENCES:",
            len(semantic_references),
        )

        return {
            "symbols": symbols,
            "relationships": relationships,
            "semantic_references": semantic_references,
        }
