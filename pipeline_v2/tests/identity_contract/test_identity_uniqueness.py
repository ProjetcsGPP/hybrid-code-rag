# pipeline_v2/tests/identity_contract/test_identity_uniqueness.py

from pipeline_v2.tests.identity_contract.identity_contract_harness import (
    IdentityContractHarness,
)


def test_identity_uniqueness(identity_registry, graph, symbol_core, relationship_core):
    harness = IdentityContractHarness(
        identity_registry, graph, symbol_core, relationship_core
    )

    result = harness.check_unique_identity()

    assert result["passed"], result["violations"]
