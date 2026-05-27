from pipeline.ast_chunker import ASTChunker

from pipeline_v2.core.symbol.symbol_core import SymbolCoreV2
from pipeline_v2.core.symbol.symbol_types import SymbolType

from pipeline_v2.core.relationship.relationship_core import RelationshipCoreV2

from pipeline_v2.core.builder.graph_builder import GraphBuilderV2
from pipeline_v2.core.builder.build_context import BuildContextV2

from pipeline_v2.core.graph.runtime_graph import graph_runtime
from pipeline_v2.core.contract.semantic_adapter import SemanticAdapter

from pipeline_v2.tests.identity_contract.identity_contract_harness import (
    IdentityContractHarness,
)

from pipeline_v2.core.identity.identity_registry import (
    IdentityRegistryV2,
)


def safe_symbol_type(value: str):
    try:
        return SymbolType(value)
    except Exception:
        return SymbolType.UNKNOWN if hasattr(SymbolType, "UNKNOWN") else value


def run_identity_contract(identity_registry, graph, symbol_core, relationship_core):

    harness = IdentityContractHarness(
        identity_registry, graph, symbol_core, relationship_core
    )

    return harness.run_all_checks()


def run_harness(file_path: str):

    # 🧹 IMPORTANT: evita estado contaminado
    graph_runtime.store.nodes.clear()
    graph_runtime.store.edges.clear()

    print("\n===== 1. AST =====")
    chunker = ASTChunker(file_path)
    chunks = chunker.chunk()

    print(f"chunks: {len(chunks)}")

    identity_registry = IdentityRegistryV2()

    print("\n===== 2. SYMBOLS =====")
    symbol_core = SymbolCoreV2(
        identity_registry=identity_registry,
    )

    symbols = []

    for c in chunks:
        meta = c["metadata"]

        print(f"Processing symbol: {meta['name']} ({meta['type']}) ({meta['file']})")

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

    print("\n===== 3. RELATIONSHIPS =====")
    rel_core = RelationshipCoreV2(
        symbol_core=symbol_core,
        identity_registry=identity_registry,
    )

    relationships = []

    for c in chunks:
        chunk_contract = SemanticAdapter.normalize_chunk(c)

        symbol_table = {s.canonical: s for s in symbols}

        relationships.extend(rel_core.process_chunk(chunk_contract, symbol_table))

    print(f"relationships: {len(relationships)}")

    print("\n===== 4. GRAPH BUILD =====")

    builder = GraphBuilderV2(identity_registry=IdentityRegistryV2())

    context = BuildContextV2(
        file_path=file_path,
        symbols=symbols,
        relationships=relationships,
    )

    graph_state = builder.ingest_file(context)

    print("graph_state:", graph_state)

    print("\n===== 5. RUNTIME GRAPH =====")
    print("nodes:", len(graph_runtime.store.nodes))
    print("edges:", len(graph_runtime.store.edges))

    print("\n===== 6. SAMPLE =====")
    for k, v in list(graph_runtime.store.nodes.items())[:3]:
        print(k, "=>", v)

    # 🔴 7. IDENTITY CONTRACT (NOVO - ESSENCIAL)
    print("\n===== 7. IDENTITY CONTRACT =====")

    result = run_identity_contract(
        identity_registry=identity_registry,
        graph=graph_runtime.store,
        symbol_core=symbol_core,
        relationship_core=rel_core,
    )

    print(result)

    from pipeline_v2.tests.harness_identity_graph_drift import (
        run_identity_graph_drift_check,
    )

    run_identity_graph_drift_check(identity_registry)


if __name__ == "__main__":
    run_harness("pipeline_v2/application/bootstrap_runtime.py")
