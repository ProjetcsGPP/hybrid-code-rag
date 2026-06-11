# pipeline_v2/core/closure/semantic_closure_loop.py


class SemanticClosureLoopV2:
    def __init__(self, identity_registry, graph_core):
        self.identity_registry = identity_registry
        self.graph_core = graph_core

    def run(self, graph_result):
        edges = graph_result.edges
        self.execute(edges)
        return graph_result

    def _rewrite_edge(self, edge, new_target):
        edge.target = new_target
        return edge

    def execute(self, edges):

        # =================================================
        # SAFETY CHECK: só roda após GraphCore consistente
        # =================================================
        if not hasattr(self.graph_core, "store"):
            return edges

        # snapshot defensivo (evita mutação indireta)
        edges = list(edges)

        classified = self._classify(edges)
        promoted = self._promote(classified)

        # aplica apenas após consistência garantida
        self._patch_graph(promoted)

        return promoted

    def _classify(self, edges):
        result = {"external": [], "unresolved": [], "strict": []}

        for e in edges:
            if e.target.startswith("UNRESOLVED::"):
                result["unresolved"].append(e)

            elif e.target.startswith("external::"):
                result["external"].append(e)

            else:
                result["strict"].append(e)

        return result

    def _promote(self, classified):
        promoted = []

        for e in classified["external"]:

            candidate = e.target.replace("external::", "")

            resolved = self.identity_registry.resolve(candidate)

            if not resolved.startswith("external::"):
                promoted.append(self._rewrite_edge(e, resolved))

        return promoted

    def _patch_graph(self, edges):
        for e in edges:
            self.graph_core.add_edge(e)
