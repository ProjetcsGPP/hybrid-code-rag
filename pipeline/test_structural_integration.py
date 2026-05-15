# pipeline/test_structural_integration.py

from collections import Counter, defaultdict
from pathlib import Path
from pprint import pformat

from pipeline.ast_chunker import ASTChunker
from pipeline.structure.structural_indexer import StructuralIndexer
from pipeline.structure.storage.sqlite_store import SQLiteStructuralStore

BASE_DIR = Path("/home/gppusrubuntu/projects/backend/apps/accounts")

EXCLUDE_DIRS = {
    "__pycache__",
    "migrations",
    ".pytest_cache",
}

OUTPUT_DIR = Path("debug_output")
OUTPUT_DIR.mkdir(exist_ok=True)


def discover_python_files(base_dir: Path):

    files = []

    for path in base_dir.rglob("*.py"):

        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue

        files.append(str(path))

    return sorted(files)


def write_output(filename, data):

    path = OUTPUT_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

    print(f"[OK] wrote: {path}")


def group_references(refs):

    grouped = defaultdict(list)

    for ref in refs:

        ref_type = ref["reference_type"]

        grouped[ref_type].append(dict(ref))

    return grouped


def build_unresolved_summary(unresolved_refs):

    counter = Counter()

    for ref in unresolved_refs:

        if "reference_name" in ref:
            counter[ref["reference_name"]] += 1

        elif "raw_call" in ref:
            counter[ref["raw_call"]] += 1

        else:
            counter["UNKNOWN"] += 1

    return counter.most_common(100)


def test_indexer():

    files = discover_python_files(BASE_DIR)

    print()
    print("========================================")
    print("FILES DISCOVERED")
    print("========================================")

    for f in files:
        print(f)

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

    print()
    print("========================================")
    print("INDEXING")
    print("========================================")

    result = indexer.index_chunks(all_chunks)

    refs = store.get_all_semantic_references()

    print("\nFIRST REF:")
    print(type(refs[0]))
    print(dict(refs[0]))

    grouped_refs = group_references(refs)

    print("\nREFERENCE TYPES:")
    print(grouped_refs.keys())

    unresolved_refs = (
        grouped_refs["UNRESOLVED_REFERENCE"]
        if "UNRESOLVED_REFERENCE" in grouped_refs
        else []
    )

    unresolved_summary = build_unresolved_summary(unresolved_refs)

    write_output(
        "symbols.txt",
        pformat(result["symbols"], width=140),
    )

    write_output(
        "relationships.txt",
        pformat(result["relationships"], width=140),
    )

    write_output(
        "references_all.txt",
        pformat([dict(r) for r in refs], width=140),
    )

    for ref_type, items in grouped_refs.items():

        filename = f"references_{ref_type.lower()}.txt"

        write_output(
            filename,
            pformat(items, width=140),
        )

    write_output(
        "unresolved_summary.txt",
        pformat(unresolved_summary, width=140),
    )

    write_output(
        "chunk_report.txt",
        pformat(chunk_report, width=140),
    )

    summary_lines = [
        "========================================",
        "STRUCTURAL TEST SUMMARY",
        "========================================",
        "",
        f"FILES: {len(files)}",
        f"TOTAL CHUNKS: {len(all_chunks)}",
        f"TOTAL SYMBOLS: {len(result['symbols'])}",
        f"TOTAL RELATIONSHIPS: {len(result['relationships'])}",
        f"TOTAL REFERENCES: {len(refs)}",
        "",
        "REFERENCE TYPES:",
    ]

    for ref_type, items in grouped_refs.items():
        summary_lines.append(f"- {ref_type}: {len(items)}")

    summary = "\n".join(summary_lines)

    write_output("summary.txt", summary)

    store.close()


if __name__ == "__main__":

    test_indexer()
