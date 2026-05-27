# pipeline_v2/core_engine/core_engine_facade.py


class CoreEngineFacade:

    def __init__(self, graph_core, query_engine, relevance_engine):
        self.graph = graph_core
        self.query = query_engine
        self.relevance = relevance_engine

    def retrieve(self, node_id: str):
        subgraph = self.query.semantic_subgraph(node_id)

        ranked = self.relevance.rank(nodes=subgraph["nodes"], edges=subgraph["edges"])

        return {"subgraph": subgraph, "ranked": ranked}
