# pipeline/structure/structural_indexer.py

from pipeline.structure.symbol_extractor import SymbolExtractor
from pipeline.structure.relationship_extractor import RelationshipExtractor
from pipeline.structure.storage.sqlite_store import SQLiteStructuralStore
from pipeline.structure.resolver.symbol_index import SymbolIndex
from pipeline.structure.resolver.symbol_resolver import SymbolResolver


class StructuralIndexer:

    def __init__(self, store: SQLiteStructuralStore):

        self.store = store

        self.symbol_extractor = SymbolExtractor()
        
        self._symbol_index = SymbolIndex()
        
        self.relationship_extractor = RelationshipExtractor(self._symbol_index)
        
        self._resolver = SymbolResolver(self._symbol_index)

        self._symbols_buffer = []

    # ---------------------------------------------
    # PASS 1 — SYMBOL EXTRACTION
    # ---------------------------------------------

    def index_chunks_pass1(self, chunks: list[dict]):

        # reset state a cada execução (evita vazamento entre runs)
        self._symbols_buffer = []
        self._symbol_index = SymbolIndex()
        self._resolver = SymbolResolver(self._symbol_index)

        symbols = []

        for chunk in chunks:

            meta = chunk.get("metadata", {})

            print("\nRAW CALLS:", meta.get("calls"))
            print("CHUNK:", meta.get("chunk_id"))

            symbol = self.symbol_extractor.extract(chunk)

            # persistência imediata (ok para now, depois podemos batch)
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

        for symbol in self._symbols_buffer:

            rels = self.relationship_extractor.extract(
                symbol,
                self._symbol_index,
                self._resolver
            )

            for r in rels:
                self.store.save_relationship(r)
                relationships.append(r)

        return relationships

    # ---------------------------------------------
    # PIPELINE ORCHESTRATOR
    # ---------------------------------------------

    def index_chunks(self, chunks: list[dict]):

        symbols = self.index_chunks_pass1(chunks)
        relationships = self.index_chunks_pass2()

        graph_stats = self.store.get_graph_stats()

        print("\nGRAPH SUMMARY:")
        print("NODES:", graph_stats["nodes"])
        print("EDGES:", graph_stats["edges"])
        print("UNRESOLVED:", graph_stats["unresolved"])

        return {
            "symbols": symbols,
            "relationships": relationships,
        }