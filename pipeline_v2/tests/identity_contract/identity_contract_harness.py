# pipeline_v2/tests/identity_contract/identity_contract_harness.py


class IdentityContractViolationError(Exception):
    pass


class IdentityContractHarness:

    def __init__(self, identity_registry, graph, symbol_core, relationship_core):
        self.identity_registry = identity_registry
        self.graph = graph
        self.symbol_core = symbol_core
        self.relationship_core = relationship_core

    def run_all_checks(self):
        results = {
            "unique_identity_check": self.check_unique_identity(),
            "registry_authority_check": self.check_registry_authority(),
            "graph_consistency_check": self.check_graph_consistency(),
            "relationship_boundaries_check": self.check_relationship_boundaries(),
        }

        if not all(r["passed"] for r in results.values()):
            raise IdentityContractViolationError(results)

        return results

    # -------------------------
    # CHECK 1
    # -------------------------
    def check_unique_identity(self):
        name_to_ids = {}

        for symbol in self.symbol_core.get_all_symbols():
            name = symbol.name
            cid = symbol.canonical_id

            name_to_ids.setdefault(name, set()).add(cid)

        violations = {
            name: list(ids) for name, ids in name_to_ids.items() if len(ids) > 1
        }

        return {"passed": len(violations) == 0, "violations": violations}

    # -------------------------
    # CHECK 2
    # -------------------------
    def check_registry_authority(self):
        violations = []

        for symbol in self.symbol_core.get_all_symbols():
            expected_id = self.identity_registry.resolve(symbol.name)

            if symbol.canonical_id != expected_id:
                violations.append(
                    {
                        "symbol": symbol.name,
                        "graph_id": symbol.canonical_id,
                        "registry_id": expected_id,
                    }
                )

        return {"passed": len(violations) == 0, "violations": violations}

    # -------------------------
    # CHECK 3
    # -------------------------
    def check_graph_consistency(self):
        violations = []

        for node in self.graph.get_nodes():
            if not self.identity_registry.exists(node.id):
                violations.append(
                    {"node_id": node.id, "reason": "node not in identity registry"}
                )

        return {"passed": len(violations) == 0, "violations": violations}

    # -------------------------
    # CHECK 4
    # -------------------------
    def check_relationship_boundaries(self):
        violations = []

        for call in self.relationship_core.get_internal_calls():

            if call.target == "IdentityRegistryV2.resolve":
                violations.append(
                    {
                        "violation": "RelationshipCore bypassed IdentityRegistry",
                        "call": str(call),
                    }
                )

        return {"passed": len(violations) == 0, "violations": violations}
