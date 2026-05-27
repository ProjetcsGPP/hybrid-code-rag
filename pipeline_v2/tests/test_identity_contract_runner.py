# pipeline_v2/tests/test_identity_contract_runner.py

from pipeline_v2.tests.identity_contract.identity_contract_harness import (
    IdentityContractHarness,
)


def run_identity_contract(identity_registry, graph, symbol_core, relationship_core):

    harness = IdentityContractHarness(
        identity_registry=identity_registry,
        graph=graph,
        symbol_core=symbol_core,
        relationship_core=relationship_core,
    )

    result = harness.run_all_checks()

    print("\n===== IDENTITY CONTRACT RESULT =====")

    for check, data in result.items():
        print(f"\n{check}")
        print("PASS:", data["passed"])
        print("VIOLATIONS:", data["violations"])

    print("\n====================================\n")
