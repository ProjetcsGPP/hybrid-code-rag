# pipeline_v2/tests/validation/test_snapshot_v3.py

import json
import pytest

# =====================================================
# HELPERS
# =====================================================


def has_runtime_objects(obj):
    """
    Detecta vazamento de objetos runtime (GraphCore, Registry, etc.)
    """
    return "object at 0x" in str(obj)


def safe_dump(snapshot: dict):
    """
    Snapshot V3 é um dict puro.
    """
    return json.dumps(snapshot, ensure_ascii=False)


def assert_is_snapshot_dict(snapshot):
    assert isinstance(snapshot, dict)
    assert "nodes" in snapshot
    assert "edges" in snapshot
    assert "metadata" in snapshot


# =====================================================
# 1. PURE SERIALIZATION TESTS
# =====================================================


def test_snapshot_is_json_serializable(snapshot):
    json_str = safe_dump(snapshot)
    assert json_str is not None
    assert len(json_str) > 0


def test_snapshot_does_not_require_default_serializer(snapshot):
    try:
        json.dumps(snapshot)
    except TypeError:
        pytest.fail("Snapshot V3 is not JSON serializable")


def test_no_python_objects_leak(snapshot):
    dump = safe_dump(snapshot)
    assert "GraphCoreV2" not in dump
    assert "IdentityRegistryV2" not in dump
    assert "ValidationContext" not in dump


def test_no_runtime_object_references(snapshot):
    assert not has_runtime_objects(snapshot.get("nodes", {}))
    assert not has_runtime_objects(snapshot.get("edges", {}))


# =====================================================
# 2. STRUCTURE INTEGRITY TESTS
# =====================================================


def test_snapshot_required_fields(snapshot):
    assert_is_snapshot_dict(snapshot)


def test_snapshot_structure_types(snapshot):

    assert isinstance(snapshot["nodes"], dict)
    assert isinstance(snapshot["edges"], dict)
    assert isinstance(snapshot["metadata"], dict)


def test_snapshot_keys_are_strings(snapshot):

    assert all(isinstance(k, str) for k in snapshot["nodes"].keys())
    assert all(isinstance(k, str) for k in snapshot["edges"].keys())


# =====================================================
# 3. DETERMINISM TESTS
# =====================================================


def test_snapshot_determinism(snapshot_engine, context):

    s1 = snapshot_engine.build(context)
    s2 = snapshot_engine.build(context)

    assert s1["nodes"] == s2["nodes"]
    assert s1["edges"] == s2["edges"]
    assert s1["metadata"] == s2["metadata"]


def test_snapshot_order_independence(snapshot_engine, context):

    original = context.graph_core.get_nodes()

    context.graph_core.nodes_data = {
        k: original[k] for k in sorted(original.keys(), reverse=True)
    }

    s1 = snapshot_engine.build(context)

    context.graph_core.nodes_data = {k: original[k] for k in sorted(original.keys())}

    s2 = snapshot_engine.build(context)

    assert s1["nodes"] == s2["nodes"]


# =====================================================
# 4. RUNTIME LEAK DETECTION (CRÍTICO)
# =====================================================


def test_no_graphcore_leak(snapshot):
    dump = safe_dump(snapshot)
    assert "GraphCoreV2" not in dump
    assert "graph_core" not in dump


def test_no_identity_registry_leak(snapshot):
    dump = safe_dump(snapshot)
    assert "IdentityRegistryV2" not in dump
    assert "identity_registry" not in dump


def test_no_validation_context_leak(snapshot):
    dump = safe_dump(snapshot)
    assert "ValidationContext" not in dump


def test_no_object_memory_references(snapshot):

    def scan(obj):
        if isinstance(obj, dict):
            return any(scan(v) for v in obj.values())
        if isinstance(obj, list):
            return any(scan(v) for v in obj)
        return has_runtime_objects(obj)

    assert not scan(snapshot.get("nodes", {}))
    assert not scan(snapshot.get("edges", {}))


# =====================================================
# 5. SNAPSHOT FINALITY TESTS
# =====================================================


def test_snapshot_is_final_artifact(snapshot_engine, context):

    snapshot = snapshot_engine.build(context)

    json.dumps(snapshot)

    assert snapshot.get("project_root") is not None


def test_snapshot_is_not_mutable_runtime_proxy(snapshot):

    assert "runtime" not in snapshot
    assert "graph_core" not in snapshot


# =====================================================
# 6. PIPELINE STABILITY TESTS
# =====================================================


def test_pipeline_snapshot_stability(run_pipeline):

    r1 = run_pipeline()
    r2 = run_pipeline()

    assert r1["graph_nodes"] == r2["graph_nodes"]
    assert r1["chunks"] == r2["chunks"]


def test_snapshot_consistency_across_runs(snapshot_engine, context):

    s1 = snapshot_engine.build(context)
    s2 = snapshot_engine.build(context)

    assert s1 == s2


# =====================================================
# 7. HARD FAILURE GUARANTEE (V3 PRINCIPLE)
# =====================================================


def test_snapshot_fails_on_invalid_objects(snapshot_engine, context):

    context.chunks.append(object())

    with pytest.raises(Exception):
        snapshot_engine.build(context)
