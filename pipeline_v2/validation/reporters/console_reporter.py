# pipeline_v2/validation/reporters/console_reporter.py

from pipeline_v2.validation.contracts.base_reporter import BaseReporter


class ConsoleReporter(BaseReporter):

    def report(self, result):

        graph = result.metrics["graph"]

        if not graph:
            return

        print()

        print("========================================")
        print("GRAPH METRICS")
        print("========================================")

        print(f"Nodes : {graph.total_nodes}")
        print(f"Edges : {graph.total_edges}")

        print()

        print("Node Types")

        for k, v in sorted(graph.node_types.items()):
            print(f"  {k:<20} {v}")

        print()

        print("Edge Types")

        for k, v in sorted(graph.edge_types.items()):
            print(f"  {k:<20} {v}")

        identity = result.metrics.get("identity")

        if identity:

            print()

            print("===== IDENTITY =====")

            print(f"Registry IDs.............{identity.registry_ids}")

            print(f"Graph Nodes..............{identity.graph_nodes}")

            print(f"Unused Registry..........{identity.unused_registry_ids}")

            print(f"Duplicate Canonicals.....{identity.duplicate_canonicals}")

            print(f"Orphan Nodes.............{identity.orphan_nodes}")

            if identity.unused_by_type:

                print()

                print("Unused Registry IDs by Type")

                for name, qty in sorted(identity.unused_by_type.items()):

                    print(f"  {name:<20} {qty}")

            if identity.orphan_by_type:

                print()

                print("Orphan Nodes by Type")

                for name, qty in sorted(identity.orphan_by_type.items()):

                    print(f"  {name:<20} {qty}")
