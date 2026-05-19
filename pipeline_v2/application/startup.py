# pipeline_v2/application/startup.py

from pipeline_v2.core.graph.runtime_graph import graph_runtime
from pipeline_v2.core.graph.graph_types import GraphNodeV2


def preload_graph():

    node = GraphNodeV2(
        id="node_1",
        type="function",
        name="test_function",
        canonical="test.test_function",
        metadata={},
    )

    graph_runtime.add_node(node)

    print("GRAPH PRELOADED")
