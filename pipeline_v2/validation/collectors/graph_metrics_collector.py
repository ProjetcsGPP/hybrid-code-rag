# pipeline_v2/validation/collectors/graph_metrics_collector.py

from collections import Counter
from pipeline_v2.validation.contracts.base_collector import BaseCollector
from pipeline_v2.validation.contracts.metrics.graph_metrics import GraphMetrics


class GraphMetricsCollectorV3(BaseCollector):

    def collect(self, context, result):

        snapshot = context.snapshot

        nodes = snapshot.nodes
        edges = snapshot.edges

        node_counter = Counter(n.get("type", "UNKNOWN") for n in nodes.values())

        edge_counter = Counter(e.get("type", "UNKNOWN") for e in edges)

        result.metrics["graph"] = GraphMetrics(
            total_nodes=len(nodes),
            total_edges=len(edges),
            node_types=dict(node_counter),
            edge_types=dict(edge_counter),
        )
