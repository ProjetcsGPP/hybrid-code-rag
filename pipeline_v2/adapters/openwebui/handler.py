# pipeline_v2/adapters/openwebui/handler.py

from pipeline_v2.core.context.context_builder import GraphContextBuilderV2


class GraphToolHandler:

    def __init__(self):
        self.builder = GraphContextBuilderV2()

    def run(self, node_id: str, depth: int = 2, filters=None):

        context = self.builder.build(node_id=node_id, depth=depth)

        # NORMALIZAÇÃO (OpenWebUI friendly)
        return {
            "focus_node": context.focus_node.__dict__,
            "nodes": [n.__dict__ for n in context.nodes],
            "edges": [e.__dict__ for e in context.edges],
            "semantic_trace": context.semantic_trace,
            "ranked_score": context.ranked_score,
            "metadata": {
                **context.metadata,
                "tool": "graph_context_v1",
                "source": "pipeline_v2",
            },
        }
