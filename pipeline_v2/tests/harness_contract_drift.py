# pipeline_v2/tests/harness_contract_drift.py

from pipeline.ast_chunker import ASTChunker

from pipeline_v2.core.symbol.symbol_core import SymbolCoreV2
from pipeline_v2.core.relationship.relationship_core import RelationshipCoreV2
from pipeline_v2.core.builder.graph_builder import GraphBuilderV2
from pipeline_v2.core.builder.build_context import BuildContextV2

from pipeline_v2.core.graph.runtime_graph import graph_runtime

from pipeline_v2.core.contract.contract_enforcer import ContractEnforcer
from pipeline_v2.core.contract.semantic_adapter import SemanticAdapter

from pipeline_v2.core.contract.symbol_adapter import SymbolAdapter
from pipeline_v2.core.contract.semantic_contract import SymbolContract


def run(file_path: str):

    print("\n===== 1. AST =====")
    chunker = ASTChunker(file_path)
    chunks = chunker.chunk()
    print("chunks:", len(chunks))

    # -------------------------
    # SYMBOLS
    # -------------------------

    print("\n===== 2. SYMBOL CONTRACT =====")

    symbol_core = SymbolCoreV2()
    symbols_contract = []
    symbols_core = []

    for c in chunks:

        meta = c["metadata"]

        clean = SymbolAdapter.from_ast(meta)

        ContractEnforcer.enforce_list(
            [clean],
            SymbolContract,
        )

        symbols_contract.append(clean)

        core_symbol = SymbolCoreV2.from_contract(clean)

        symbol_core.register(core_symbol)

        symbols_core.append(core_symbol)

        print(f"Processing symbol: {clean.name} ({clean.type}) ({clean.file_path})")

    print("contracts:", len(symbols_contract))
    print("core:", len(symbols_core))

    # -------------------------
    # RELATIONSHIPS
    # -------------------------
    print("\n===== 3. RELATIONSHIP CONTRACT =====")

    rel_core = RelationshipCoreV2(symbol_core=symbol_core)

    relationships = []

    for c in chunks:

        chunk_contract = SemanticAdapter.normalize_chunk(c)

        rels = rel_core.process_chunk(chunk_contract, {})

        for r in rels:
            r = ContractEnforcer.enforce_relationship(r)
            relationships.append(r)

    print("relationships:", len(relationships))

    # -------------------------
    # GRAPH BUILD
    # -------------------------
    print("\n===== 4. GRAPH BUILD =====")

    builder = GraphBuilderV2()

    context = BuildContextV2(
        file_path=file_path,
        symbols=symbols_core,
        relationships=relationships,
    )

    graph_state = builder.ingest_file(context)

    print("nodes:", graph_state["nodes_created"])
    print("edges:", graph_state["edges_created"])

    # -------------------------
    # DRIFT ANALYSIS
    # -------------------------
    print("\n===== 5. DRIFT DETECTION =====")

    graph_nodes = len(graph_runtime.store.nodes)
    graph_edges = len(graph_runtime.store.edges)

    symbol_count = len(symbols_core)
    rel_count = len(relationships)

    drift_report = {
        "symbol_vs_graph_nodes": symbol_count - graph_nodes,
        "relationship_vs_graph_edges": rel_count - graph_edges,
    }

    print(drift_report)

    if drift_report["symbol_vs_graph_nodes"] != 0:
        print("⚠️ DRIFT DETECTADO: símbolos ≠ nós do grafo")

    if drift_report["relationship_vs_graph_edges"] != 0:
        print("⚠️ DRIFT DETECTADO: relações ≠ edges do grafo")

    if (
        drift_report["symbol_vs_graph_nodes"] == 0
        and drift_report["relationship_vs_graph_edges"] == 0
    ):
        print("✅ SEM DRIFT: pipeline consistente")

    # -------------------------
    # SAMPLE OUTPUT
    # -------------------------
    print("\n===== 6. SAMPLE NODES =====")

    for k, v in list(graph_runtime.store.nodes.items())[:3]:
        print(k, "=>", v)

    print("\n===== 7. RELATIONSHIP SAMPLE =====")

    for r in relationships[:5]:

        print(
            {
                "id": r.id,
                "type": r.type,
                "dispatch": r.dispatch,
                "confidence": r.confidence,
                "semantic_owner": r.semantic_owner,
                "resolved_call": r.metadata.get("resolved_call"),
                "metadata": r.metadata,
            }
        )

    print("\n===== 8. INSTANCE SEMANTIC CHECK =====")

    for r in relationships:

        if r.semantic_owner:

            print(
                {
                    "type": r.type,
                    "semantic_owner": r.semantic_owner,
                    "confidence": r.confidence,
                    "resolved_call": r.metadata.get("resolved_call"),
                    "provenance": r.provenance,
                }
            )


if __name__ == "__main__":
    run("pipeline_v2/application/bootstrap_runtime.py")
