# pipeline_v2/validation/collectors/identity_metrics_collector.py

from collections import Counter
from pipeline_v2.validation.contracts.base_collector import BaseCollector
from pipeline_v2.validation.contracts.metrics.identity_metrics import IdentityMetrics


class IdentityMetricsCollectorV3(BaseCollector):

    def collect(self, context, result):

        snapshot = context.snapshot

        registry = snapshot.registry
        nodes = snapshot.nodes

        registry_ids = set(registry.keys())
        graph_ids = set(nodes.keys())

        unused = registry_ids - graph_ids
        orphan = graph_ids - registry_ids

        unused_counter = Counter()
        orphan_counter = Counter()

        for rid in unused:
            symbol = registry.get(rid, {})
            symbol_type = symbol.get("type", "UNKNOWN")
            unused_counter[str(symbol_type)] += 1

        for nid in orphan:
            node = nodes.get(nid, {})
            orphan_counter[node.get("type", "UNKNOWN")] += 1

        canonical_counter = Counter()

        for symbol in registry.values():
            canonical = symbol.get("canonical")
            if canonical:
                canonical_counter[canonical] += 1

        duplicate_canonicals = sum(
            count - 1 for count in canonical_counter.values() if count > 1
        )

        result.metrics["identity"] = IdentityMetrics(
            registry_ids=len(registry_ids),
            graph_nodes=len(graph_ids),
            unused_registry_ids=len(unused),
            duplicate_ids=0,
            duplicate_canonicals=duplicate_canonicals,
            orphan_nodes=len(orphan),
            unused_by_type=dict(unused_counter),
            orphan_by_type=dict(orphan_counter),
        )
