# pipeline_v2/tests/identity_contract/test_identity_registry_authority.py

from pipeline_v2.tests.identity_contract.identity_contract_harness import (
    IdentityContractHarness,
)


def test_registry_authority(identity_registry, graph, symbol_core, relationship_core):
    harness = IdentityContractHarness(
        identity_registry, graph, symbol_core, relationship_core
    )

    result = harness.check_registry_authority()

    assert result["passed"], result["violations"]
