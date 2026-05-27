# pipeline/test_structural_indexer.py

from pipeline.ast_chunker import ASTChunker

# from pipeline.structure.structural_indexer import StructuralIndexer
from pipeline.structure.storage.sqlite_store import SQLiteStructuralStore
from pipeline_v2.application.bootstrap_legacy_bridge import (
    build_legacy_indexer_with_postgres,
)


def test_indexer(file_path: str):

    chunker = ASTChunker(file_path)

    chunks = chunker.chunk()

    store = SQLiteStructuralStore()

    store.reset()

    # indexer = StructuralIndexer(store)
    indexer = build_legacy_indexer_with_postgres()

    result = indexer.index_chunks(chunks)

    print()
    print("================ SYMBOLS ================")

    for s in result["symbols"]:
        print(s)

    print()
    print("============ RELATIONSHIPS =============")

    for r in result["relationships"]:
        print(r)

    print("\n============ REFERENCES ============")

    for ref in result["semantic_references"]:
        print(ref)

    store.close()


if __name__ == "__main__":

    test_indexer("/home/gppusrubuntu/projects/backend/apps/accounts/models.py")
