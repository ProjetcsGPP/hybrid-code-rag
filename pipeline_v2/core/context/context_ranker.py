# pipeline_v2/core/context/context_ranker.py


class GraphContextRankerV2:
    """
    Responsável por ordenar relevância do subgrafo.
    Não depende de ML ainda — mas já preparado para isso.
    """

    def rank_nodes(self, nodes, focus_node_id: str):
        ranked = []

        for n in nodes:
            score = 1.0

            if n.id == focus_node_id:
                score += 10

            # heurística simples inicial (extensível)
            if hasattr(n, "metadata") and n.metadata:
                score += len(n.metadata) * 0.1

            ranked.append((n, score))

        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked

    def rank_edges(self, edges):
        ranked = []

        for e in edges:
            score = getattr(e, "confidence", 1.0)

            if getattr(e, "layer", None) == "SEMANTIC":
                score += 0.5

            if getattr(e, "status", None) == "RESOLVED":
                score += 0.3

            ranked.append((e, score))

        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked
