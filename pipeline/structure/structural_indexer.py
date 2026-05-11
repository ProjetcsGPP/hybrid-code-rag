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
        self.relationship_extractor = RelationshipExtractor()

        self._symbols_buffer = []

        self._symbol_index = SymbolIndex()
        self._resolver = SymbolResolver(self._symbol_index)

    def index_chunks_pass1(self, chunks: list[dict]):

        self._symbols_buffer = []

        symbols = []

        for chunk in chunks:

            print("\nRAW CALLS:", chunk["metadata"].get("calls"))
            print("CHUNK:", chunk["metadata"].get("chunk_id"))
            
            symbol = self.symbol_extractor.extract(chunk)

            self.store.save_symbol(symbol)

            self._symbols_buffer.append(symbol)
            symbols.append(symbol)

            self._symbol_index.add(symbol)
            

        return symbols

    def index_chunks_pass2(self):

        relationships = []

        for symbol in self._symbols_buffer:

            rels = self.relationship_extractor.extract(
                symbol,
                self._symbol_index
            )

            for r in rels:
                self.store.save_relationship(r)
                relationships.append(r)

        return relationships

    def index_chunks(self, chunks: list[dict]):

        self.index_chunks_pass1(chunks)
        relationships = self.index_chunks_pass2()

        return {
            "symbols": self._symbols_buffer,
            "relationships": relationships,
        }