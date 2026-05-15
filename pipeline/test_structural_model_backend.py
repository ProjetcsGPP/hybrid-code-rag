# pipeline/test_structural_model_backend.py

from pathlib import Path
from pprint import pformat

from pipeline.ast_chunker import ASTChunker
from pipeline.structure.structural_indexer import StructuralIndexer
from pipeline.structure.storage.sqlite_store import SQLiteStructuralStore

FILES = [
    "/home/gppusrubuntu/projects/backend/apps/accounts/models.py",
    "/home/gppusrubuntu/projects/backend/apps/accounts/views.py",
    "/home/gppusrubuntu/projects/backend/apps/accounts/middleware.py",
    "/home/gppusrubuntu/projects/backend/apps/accounts/"
    "services/application_registry.py",
]


OUTPUT_DIR = Path("debug_output")
OUTPUT_DIR.mkdir(exist_ok=True)


def write_output(filename, data):

    path = OUTPUT_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

    print(f"[OK] wrote: {path}")


def test_indexer(files):

    store = SQLiteStructuralStore()
    store.reset()

    indexer = StructuralIndexer(store)

    all_chunks = []

    chunk_report = []

    for file_path in files:

        print(f"\nCHUNKING: {file_path}")

        chunker = ASTChunker(file_path)

        chunks = chunker.chunk()

        chunk_report.append(
            {
                "file": file_path,
                "chunks": len(chunks),
            }
        )

        all_chunks.extend(chunks)

    result = indexer.index_chunks(all_chunks)

    refs = store.get_all_semantic_references()

    write_output(
        "symbols.txt",
        pformat(result["symbols"], width=120),
    )

    write_output(
        "relationships.txt",
        pformat(result["relationships"], width=120),
    )

    write_output(
        "references.txt",
        pformat(refs, width=120),
    )

    write_output(
        "chunk_report.txt",
        pformat(chunk_report, width=120),
    )

    summary = f"""
TOTAL CHUNKS: {len(all_chunks)}
TOTAL SYMBOLS: {len(result["symbols"])}
TOTAL RELATIONSHIPS: {len(result["relationships"])}
TOTAL REFERENCES: {len(refs)}
"""

    write_output("summary.txt", summary)

    store.close()


if __name__ == "__main__":

    test_indexer(FILES)
