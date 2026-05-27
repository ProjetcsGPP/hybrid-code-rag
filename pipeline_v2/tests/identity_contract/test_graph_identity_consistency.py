# pipeline_v2/tests/identity_contract/test_graph_identity_consistency.py

from pipeline_v2.tests.identity_contract.identity_contract_harness import (
    IdentityContractHarness,
)


def test_graph_identity_consistency(
    identity_registry, graph, symbol_core, relationship_core
):
    harness = IdentityContractHarness(
        identity_registry, graph, symbol_core, relationship_core
    )

    result = harness.check_graph_consistency()

    assert result["passed"], result["violations"]
