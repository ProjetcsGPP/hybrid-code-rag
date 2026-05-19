# pipeline_v2/application/bootstrap_runtime.py

from pipeline_v2.core.graph.runtime_graph import graph_runtime
from pipeline_v2.core.graph.graph_types import GraphNodeV2


def bootstrap_runtime():

    node = GraphNodeV2(
        id="node_1",
        type="function",
        name="test_function",
        canonical="test.test_function",
    )

    graph_runtime.add_node(node)
