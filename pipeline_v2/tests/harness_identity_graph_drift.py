# pipeline_v2/tests/harness_identity_graph_drift.py

from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2


def run_identity_graph_drift_check(
    identity_registry: IdentityRegistryV2,
    graph_runtime,
):

    print("\n===== IDENTITY vs GRAPH DRIFT CHECK =====")

    registry_ids = {
        rid
        for rid in identity_registry.by_id.keys()
        if "::CALLS::" not in rid and "::FRAMEWORK_CALL::" not in rid
    }
    graph_ids = set(graph_runtime.store.nodes.keys())

    # -------------------------
    # 1. MISSING IN GRAPH
    # -------------------------
    missing_in_graph = registry_ids - graph_ids

    # -------------------------
    # 2. ORPHAN NODES (no registry)
    # -------------------------
    orphan_nodes = graph_ids - registry_ids

    # -------------------------
    # 3. CONSISTENCY SCORE
    # -------------------------
    total = len(registry_ids.union(graph_ids)) or 1
    consistent = len(registry_ids.intersection(graph_ids))

    score = consistent / total

    print(f"Registry IDs: {len(registry_ids)}")
    print(f"Graph Nodes: {len(graph_ids)}")

    print(f"Missing in Graph: {len(missing_in_graph)}")
    print(f"Orphan Nodes: {len(orphan_nodes)}")

    print(f"Consistency Score: {score:.2%}")

    if missing_in_graph:
        print("\n--- Missing in Graph ---")
        for x in list(missing_in_graph)[:20]:
            print(x)

    if orphan_nodes:
        print("\n--- Orphan Nodes ---")
        for x in list(orphan_nodes)[:20]:
            print(x)

    return {
        "missing_in_graph": list(missing_in_graph),
        "missing_in_registry": list(orphan_nodes),
        "passed": len(missing_in_graph) == 0 and len(orphan_nodes) == 0,
    }
