# pipeline_v2/core/graph/graph_query.py


class GraphQueryV2:
    def __init__(self, graph_core):
        self.graph = graph_core

    def find_dependencies(self, node_id: str):
        return self.graph.store.get_edges_from(node_id)

    def find_references(self, node_id: str):
        return self.graph.store.get_edges_to(node_id)
