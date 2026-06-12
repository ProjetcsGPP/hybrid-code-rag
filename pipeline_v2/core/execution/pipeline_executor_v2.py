# pipeline_v2/core/execution/pipeline_executor_v2.py

from dataclasses import replace


class PipelineExecutorV2:

    def __init__(self, graph_core, stabilizer, closure_loop):
        self.graph_core = graph_core
        self.stabilizer = stabilizer
        self.closure_loop = closure_loop

    def run(self, graph_result):

        # 1. STABILIZE (semântica ainda livre)
        edges = self.stabilizer.stabilize(graph_result.edges)

        graph_result = replace(graph_result, edges=edges)

        # 2. COMMIT NO GRAPH CORE (OBRIGATÓRIO ANTES DO CLOSURE)
        self._commit(graph_result)

        # 3. CLOSURE SÓ AQUI (SAFE POINT)
        closure_result = self.closure_loop.execute(graph_result.edges)

        # 4. APPLY CLOSURE RESULTS
        for edge in closure_result:
            self.graph_core.add_edge(edge)

        return self.graph_core

    def _commit(self, graph_result):

        for node in graph_result.nodes:
            self.graph_core.add_node(node)

        for edge in graph_result.edges:
            self.graph_core.add_edge(edge)
