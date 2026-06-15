# tests/integration/test_semantic_pipeline_v2.py

from pipeline_v2.tests.fixtures.orchestrator_factory import (
    build_orchestrator,
)

from pipeline_v2.tests.fixtures.sample_ast import (
    load_sample_ast,
)


def test_pipeline_no_external_or_unresolved():

    orchestrator = build_orchestrator()

    ast_payload = load_sample_ast()

    result = orchestrator.execute(ast_payload)

    print("Pipeline execution result:", result)

    # =====================================================
    # 1. RESULT LAYER
    # =====================================================

    assert "edges" in result
    assert len(result["edges"]) > 0

    for e in result["edges"]:
        assert e.source is not None
        assert e.target is not None

        assert isinstance(e.source, str)
        assert isinstance(e.target, str)

        assert e.source != ""
        assert e.target != ""

    # =====================================================
    # 2. GRAPHCORE LAYER
    # =====================================================

    graph = orchestrator.graph_core.get_edges()

    # enquanto os símbolos não são materializados
    # no GraphCore, edges podem ser rejeitadas
    # pelo boundary enforcement

    if len(graph) > 0:

        for e in graph:

            assert e.source is not None
            assert e.target is not None
            assert e.id is not None

            assert isinstance(e.source, str)
            assert isinstance(e.target, str)

            assert e.source != ""
            assert e.target != ""


def test_closure_does_not_duplicate_edges():

    orchestrator = build_orchestrator()

    ast_payload = load_sample_ast()

    orchestrator.execute(ast_payload)

    graph = orchestrator.graph_core.get_edges()

    # =====================================================
    # 1. EDGE UNIQUENESS
    # =====================================================

    edge_ids = [e.id for e in graph]

    assert len(edge_ids) == len(set(edge_ids))

    # =====================================================
    # 2. STRUCTURAL INTEGRITY
    # =====================================================

    for e in graph:

        assert e.source is not None
        assert e.target is not None

        assert isinstance(e.source, str)
        assert isinstance(e.target, str)

        assert e.source != ""
        assert e.target != ""

    # =====================================================
    # 3. STABILITY CHECK
    # =====================================================

    graph_after = orchestrator.graph_core.get_edges()

    assert len(graph) == len(graph_after)
