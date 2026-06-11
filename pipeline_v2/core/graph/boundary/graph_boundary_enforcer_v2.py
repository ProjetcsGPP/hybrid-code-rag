# pipeline_v2/core/graph/boundary/graph_boundary_enforcer_v2.py


class GraphBoundaryEnforcerV2:
    """
    ÚNICO ponto de controle de entrada do GraphCore.

    Responsável por:
    - bloquear dirty nodes/edges
    - normalizar external::
    - impedir unresolved leak
    """

    def allow_node(self, node_id: str, node=None):

        if not node_id:
            return False

        if node_id.startswith("UNRESOLVED::"):
            return False

        return True

    def allow_edge(self, edge):

        if not edge:
            return False

        source = str(edge.source)
        target = str(edge.target)

        # bloqueio hard
        if source.startswith("UNRESOLVED::") or target.startswith("UNRESOLVED::"):
            return False

        # external NÃO entra como edge endpoint
        if source.startswith("external::") or target.startswith("external::"):
            return False

        return True

    def normalize_node(self, node):

        # hook futuro (ex: external lazy materialization)
        return node

    def normalize_edge(self, edge):
        return edge
