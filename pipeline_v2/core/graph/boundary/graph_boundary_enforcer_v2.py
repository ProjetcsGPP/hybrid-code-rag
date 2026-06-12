# pipeline_v2/core/graph/boundary/graph_boundary_enforcer_v2.py


class GraphBoundaryEnforcerV2:

    def allow_node(self, node_id: str, node=None):

        if not node_id:
            return False

        return isinstance(node_id, str)

    def allow_edge(self, edge):

        if not edge:
            return False

        source = edge.source
        target = edge.target

        if source is None or target is None:
            return False

        # ResolutionEvent nunca atravessa a fronteira
        if hasattr(source, "event_type"):
            raise ValueError(f"ResolutionEvent leaked into graph boundary: {source}")

        if hasattr(target, "event_type"):
            raise ValueError(f"ResolutionEvent leaked into graph boundary: {target}")

        return True

    def normalize_node(self, node):
        return node

    def normalize_edge(self, edge):
        return edge
