# pipeline_v2/core/closure/semantic_closure_loop.py


class SemanticClosureLoopV2:

    def __init__(self, identity_registry, graph_core):
        self.identity_registry = identity_registry
        self.graph_core = graph_core

    def run(self, graph_result):
        return graph_result

    def execute(self, edges):
        return edges
