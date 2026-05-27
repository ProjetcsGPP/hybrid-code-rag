# pipeline_v2/tests/identity_contract/test_relationship_resolution_boundaries.py

from pipeline_v2.tests.identity_contract.identity_contract_harness import (
    IdentityContractHarness,
)


def test_relationship_boundaries(
    identity_registry, graph, symbol_core, relationship_core
):
    harness = IdentityContractHarness(
        identity_registry, graph, symbol_core, relationship_core
    )

    result = harness.check_relationship_boundaries()

    assert result["passed"], result["violations"]
