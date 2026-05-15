# pipeline/test_structural_runtime.py

from pipeline.ast_chunker import ASTChunker
from pipeline.structure.resolver.symbol_index import SymbolIndex

from pipeline.structure import (
    SymbolExtractor,
    RelationshipExtractor,
)


def test_structural_runtime(file_path: str):

    chunker = ASTChunker(file_path)
    chunks = chunker.chunk()

    symbol_index = SymbolIndex()

    symbol_extractor = SymbolExtractor()

    relationship_extractor = RelationshipExtractor(symbol_index)

    symbols = []
    relationships = []

    for chunk in chunks:

        symbol = symbol_extractor.extract(chunk)

        symbols.append(symbol)

        symbol_index.add(symbol)   # 🔴 ESSENCIAL

        rels, _ = relationship_extractor.extract(symbol, symbol_index)

        relationships.extend(rels)

    print("\n================ SYMBOLS ================")
    for s in symbols:
        print(s)

    print("\n============ RELATIONSHIPS =============")
    for r in relationships:
        print(r)