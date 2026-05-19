# test_graph.py

from pipeline_v2.core.graph.runtime_graph import graph_runtime

from pipeline_v2.core.graph.graph_types import GraphNodeV2

from pipeline_v2.core.context.context_builder import (
    GraphContextBuilderV2,
)

node = GraphNodeV2(
    id="node_1",
    type="function",
    name="test_function",
    canonical="test.test_function",
)

graph_runtime.add_node(node)

builder = GraphContextBuilderV2()

context = builder.build("node_1")

print(context)
