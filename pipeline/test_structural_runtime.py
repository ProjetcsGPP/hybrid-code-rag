from pipeline.ast_chunker import ASTChunker

from pipeline.structure import (
    SymbolExtractor,
    RelationshipExtractor,
)


def test_structural_runtime(file_path: str):

    chunker = ASTChunker(file_path)

    chunks = chunker.chunk()

    symbol_extractor = SymbolExtractor()

    relationship_extractor = (
        RelationshipExtractor()
    )

    symbols = []

    relationships = []

    for chunk in chunks:

        symbol = symbol_extractor.extract(
            chunk
        )

        symbols.append(symbol)

        rels = relationship_extractor.extract(
            symbol
        )

        relationships.extend(rels)

    print()
    print("================ SYMBOLS ================")

    for s in symbols:
        print(s)

    print()
    print("============ RELATIONSHIPS =============")

    for r in relationships:
        print(r)


if __name__ == "__main__":

    test_structural_runtime(
        "/home/gppusrubuntu/projects/backend/apps/accounts/models.py"
    )