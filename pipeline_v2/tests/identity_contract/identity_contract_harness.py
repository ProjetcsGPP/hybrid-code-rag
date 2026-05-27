from pipeline_v2.core.identity.identity_reader_v1 import IdentityReaderV1


class IdentityContractViolationError(Exception):
    pass


class IdentityContractHarness:

    def __init__(
        self,
        identity_registry,
        graph,
        symbol_core,
        relationship_core,
    ):

        self.identity_registry = identity_registry
        self.reader = IdentityReaderV1(identity_registry)

        self.graph = graph
        self.symbol_core = symbol_core
        self.relationship_core = relationship_core

    # =====================================================
    # MAIN
    # =====================================================

    def run_all_checks(self):

        results = {
            "unique_identity_check": self.check_unique_identity(),
            "registry_authority_check": self.check_registry_authority(),
            "graph_consistency_check": self.check_graph_consistency(),
            "relationship_boundaries_check": self.check_relationship_boundaries(),
        }

        failed = [k for k, v in results.items() if not v["passed"]]

        if failed:
            raise IdentityContractViolationError(results)

        return results

    # =====================================================
    # CHECK 1 - UNIQUE SYMBOL IDENTITY
    # =====================================================

    def check_unique_identity(self):

        name_to_ids = {}

        for symbol in self.reader.iter_symbols():

            name_to_ids.setdefault(symbol.name, set()).add(symbol.id)

        violations = {
            name: list(ids) for name, ids in name_to_ids.items() if len(ids) > 1
        }

        return {
            "passed": len(violations) == 0,
            "violations": violations,
        }

    # =====================================================
    # CHECK 2 - REGISTRY AUTHORITY
    # =====================================================

    def check_registry_authority(self):

        violations = []

        for symbol in self.symbol_core.get_all_symbols():

            if symbol.id not in self.identity_registry.by_id:

                violations.append(
                    {
                        "symbol": symbol.name,
                        "id": symbol.id,
                        "reason": "symbol missing in registry",
                    }
                )

        return {
            "passed": len(violations) == 0,
            "violations": violations,
        }

    # =====================================================
    # CHECK 3 - GRAPH CONSISTENCY
    # =====================================================

    def check_graph_consistency(self):

        violations = []

        for node in self.graph.nodes.values():

            if node.id not in self.identity_registry.by_id:

                violations.append(
                    {
                        "node_id": node.id,
                        "reason": "node not registered",
                    }
                )

        return {
            "passed": len(violations) == 0,
            "violations": violations,
        }

    # =====================================================
    # CHECK 4 - RELATIONSHIP BOUNDARIES
    # =====================================================

    def check_relationship_boundaries(self):

        violations = []

        for edge in self.graph.edges.values():

            if edge.source == edge.target:
                violations.append(
                    {
                        "edge": edge.id,
                        "reason": "self-reference detected",
                    }
                )
                continue

            if edge.source not in self.identity_registry.by_id:
                violations.append(
                    {
                        "edge": edge.id,
                        "reason": "source missing in identity registry",
                    }
                )

            if edge.target not in self.identity_registry.by_id:
                violations.append(
                    {
                        "edge": edge.id,
                        "reason": "target missing in identity registry",
                    }
                )

        return {
            "passed": len(violations) == 0,
            "violations": violations,
        }
