from pipeline.ast_chunker import ASTChunker
from pipeline.structure.structural_indexer import StructuralIndexer
from pipeline.structure.storage.sqlite_store import SQLiteStructuralStore


def test_indexer(file_path: str):

    chunker = ASTChunker(file_path)

    chunks = chunker.chunk()

    store = SQLiteStructuralStore()
    
    store.reset()

    indexer = StructuralIndexer(store)

    result = indexer.index_chunks(chunks)

    print()
    print("================ SYMBOLS ================")

    for s in result["symbols"]:
        print(s)

    print()
    print("============ RELATIONSHIPS =============")

    for r in result["relationships"]:
        print(r)

    store.close()


if __name__ == "__main__":

    test_indexer(
        "/home/gppusrubuntu/projects/backend/apps/accounts/models.py"
    )