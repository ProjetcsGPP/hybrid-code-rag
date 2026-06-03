# pipeline_v2/tests/project_ingestion_v2.py

import os
from pathlib import Path
from typing import List

import json

from pipeline.ast_chunker import ASTChunker

from pipeline_v2.application.bootstrap_runtime import create_runtime_context

from pipeline_v2.core.symbol.symbol_core import SymbolCoreV2
from pipeline_v2.core.symbol.symbol_types import SymbolType

from pipeline_v2.core.relationship.relationship_core import RelationshipCoreV2

from pipeline_v2.core.builder.graph_builder import GraphBuilderV2
from pipeline_v2.core.builder.build_context import BuildContextV2

from pipeline_v2.core.contract.semantic_adapter import SemanticAdapter

from pipeline_v2.core.audit.identity_graph_auditor_v2 import IdentityGraphAuditorV2

from pipeline_v2.tests.identity_contract.identity_contract_harness import (
    IdentityContractHarness,
)

# =====================================================
# CONFIG
# =====================================================

DEFAULT_IGNORE_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    "migrations",
    "node_modules",
}

DEFAULT_EXTENSIONS = {".py"}


# =====================================================
# FILE SCANNER
# =====================================================


def scan_project_files(root_path: str) -> List[str]:
    files = []

    for base, dirs, filenames in os.walk(root_path):

        # prune dirs
        dirs[:] = [d for d in dirs if d not in DEFAULT_IGNORE_DIRS]

        for f in filenames:
            if Path(f).suffix in DEFAULT_EXTENSIONS:
                files.append(os.path.join(base, f))

    return sorted(files)


# =====================================================
# SAFE SYMBOL TYPE
# =====================================================


def safe_symbol_type(value: str):
    try:
        return SymbolType(value)
    except Exception:
        return SymbolType.UNKNOWN if hasattr(SymbolType, "UNKNOWN") else value


# =====================================================
# MAIN PIPELINE
# =====================================================


def run_project_ingestion(project_root: str):
    print("\n====================================")
    print("🚀 CODE-RAG V2 PROJECT INGESTION")
    print("====================================\n")

    # -------------------------
    # RUNTIME
    # -------------------------
    runtime = create_runtime_context()
    identity_registry = runtime.identity_registry
    graph_runtime = runtime.graph_runtime

    # reset determinístico
    runtime.reset()

    # -------------------------
    # FILES
    # -------------------------
    files = scan_project_files(project_root)

    print(f"📁 Files found: {len(files)}")

    all_chunks = []

    # -------------------------
    # AST PHASE
    # -------------------------
    print("\n===== 1. AST CHUNKING =====")

    for f in files:
        try:
            chunker = ASTChunker(f)
            chunks = chunker.chunk()

            all_chunks.extend(chunks)

            print(f"[OK] {f} -> {len(chunks)} chunks")

        except Exception as e:
            print(f"[SKIP] {f} -> {e}")

    print(f"\nTOTAL CHUNKS: {len(all_chunks)}")

    # -------------------------
    # SYMBOL PHASE
    # -------------------------
    print("\n===== 2. SYMBOL EXTRACTION =====")

    symbol_core = SymbolCoreV2(identity_registry=identity_registry)

    symbols = []

    for c in all_chunks:
        meta = c["metadata"]

        sym = symbol_core.create_symbol(
            name=meta["name"],
            type=safe_symbol_type(meta["type"]),
            file_path=meta["file"],
            canonical=meta.get("symbol_path"),
            metadata={
                k: v for k, v in meta.items() if k not in ["name", "type", "file"]
            },
        )

        symbols.append(sym)

    print(f"TOTAL SYMBOLS: {len(symbols)}")

    # -------------------------
    # RELATIONSHIP PHASE
    # -------------------------
    print("\n===== 3. RELATIONSHIPS =====")

    rel_core = RelationshipCoreV2(
        symbol_core=symbol_core,
        identity_registry=identity_registry,
    )

    relationships = []

    for c in all_chunks:
        chunk_contract = SemanticAdapter.normalize_chunk(c)

        rels = rel_core.process_chunk(chunk_contract, {})

        relationships.extend(rels)

    print(f"TOTAL RELATIONSHIPS: {len(relationships)}")

    # -------------------------
    # GRAPH BUILD PHASE
    # -------------------------
    print("\n===== 4. GRAPH BUILD =====")

    builder = GraphBuilderV2(
        identity_registry=identity_registry,
        graph_core=graph_runtime,
    )

    context = BuildContextV2(
        file_path=project_root,
        symbols=symbols,
        relationships=relationships,
    )

    graph_state = builder.ingest_file(context)

    print("GRAPH STATE:", graph_state)

    # -------------------------
    # GRAPH STATS
    # -------------------------
    print("\n===== 5. GRAPH SUMMARY =====")

    print("Nodes:", len(graph_runtime.store.nodes))
    print("Edges:", len(graph_runtime.store.edges))
    print("Registry IDs:", len(identity_registry.by_id))

    # -------------------------
    # IDENTITY CONTRACT
    # -------------------------
    print("\n===== 6. IDENTITY CONTRACT =====")

    harness = IdentityContractHarness(
        identity_registry,
        graph_runtime.store,
        symbol_core,
        rel_core,
    )

    contract_result = harness.run_all_checks()

    print(contract_result)

    # -------------------------
    # AUDITOR (FINAL TRUTH)
    # -------------------------
    print("\n===== 7. IDENTITY GRAPH AUDIT =====")

    auditor = IdentityGraphAuditorV2()

    report = auditor.audit(
        identity_registry=identity_registry,
        graph_store=graph_runtime.store,
    )

    print("\n--- FINAL REPORT ---")
    print(report)

    with open("report_artifacts/external_nodes.json", "w", encoding="utf-8") as f:

        json.dump(
            report.external_nodes,
            f,
            indent=2,
            ensure_ascii=False,
        )

    # -------------------------
    # RETURN
    # -------------------------
    return {
        "files": len(files),
        "chunks": len(all_chunks),
        "symbols": len(symbols),
        "relationships": len(relationships),
        "graph_nodes": len(graph_runtime.store.nodes),
        "graph_edges": len(graph_runtime.store.edges),
        "contract": contract_result,
        "audit": report,
    }


# =====================================================
# CLI
# =====================================================

if __name__ == "__main__":

    PROJECT_ROOT = "/home/gppusrubuntu/projects/backend"

    result = run_project_ingestion(PROJECT_ROOT)

    print("\n====================================")
    print("🏁 FINAL RESULT")
    print("====================================")
    print(result)
