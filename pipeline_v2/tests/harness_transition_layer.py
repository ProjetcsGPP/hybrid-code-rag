# pipeline_v2/tests/harness_transition_layer.py

from pipeline.ast_chunker import ASTChunker

from pipeline_v2.core.symbol.symbol_core import SymbolCoreV2
from pipeline_v2.core.relationship.relationship_core import RelationshipCoreV2
from pipeline_v2.core.builder.graph_builder import GraphBuilderV2
from pipeline_v2.core.builder.build_context import BuildContextV2

from pipeline_v2.core.contract.contract_enforcer import ContractEnforcer

from pipeline_v2.core.contract.symbol_adapter import SymbolAdapter

from pipeline_v2.core.contract.semantic_contract import SymbolContract
from pipeline_v2.core.contract.semantic_adapter import SemanticAdapter

from pipeline_v2.application.bootstrap_runtime import (
    identity_registry,
    graph_runtime,
)


def run(file_path: str):

    print("\n===== 1. AST =====")
    chunks = ASTChunker(file_path).chunk()

    print("\n===== 2. SYMBOL TRANSITION LAYER =====")

    symbol_core = SymbolCoreV2(
        identity_registry=identity_registry,
    )
    symbols_contract = []
    symbols_core = []

    for c in chunks:

        meta = c["metadata"]

        contract_symbol = SymbolAdapter.from_ast(meta)

        ContractEnforcer.enforce_list(
            [contract_symbol],
            SymbolContract,
        )

        core_symbol = symbol_core.create_symbol(
            name=contract_symbol.name,
            type=contract_symbol.type,
            file_path=contract_symbol.file_path,
            canonical=contract_symbol.canonical,
            metadata=getattr(contract_symbol, "metadata", {}),
        )

        symbols_contract.append(contract_symbol)
        symbols_core.append(core_symbol)

        print(f"{core_symbol.name} OK")

    print("\n===== 3. RELATIONSHIPS =====")

    rel_core = RelationshipCoreV2(
        symbol_core=symbol_core,
        identity_registry=identity_registry,
    )

    relationships = []

    for c in chunks:

        chunk_contract = SemanticAdapter.normalize_chunk(c)

        rels = rel_core.process_chunk(
            chunk_contract,
            {s.name: s for s in symbols_core},
        )
        relationships.extend(rels)

    print("relationships:", len(relationships))

    print("\n===== 4. GRAPH BUILD =====")

    builder = GraphBuilderV2(
        identity_registry=identity_registry,
        graph_core=graph_runtime,
    )

    context = BuildContextV2(
        file_path=file_path,
        symbols=symbols_core,
        relationships=relationships,
    )

    graph_state = builder.ingest_file(context)

    print(graph_state)

    print("\n===== 5. TRANSITION VALIDATION =====")

    print("contract:", len(symbols_contract))
    print("core:", len(symbols_core))
    print("rels:", len(relationships))


if __name__ == "__main__":
    run("pipeline_v2/application/bootstrap_runtime.py")
