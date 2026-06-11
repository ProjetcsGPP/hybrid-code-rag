# pipeline_v2/core/context/context_assembly_engine_v2.py


from typing import Dict, List, Optional

from pipeline_v2.core.contract.graph_contracts import GraphSubgraphV2


class ContextAssemblyEngineV2:
    """
    Context Assembly Engine V2

    Converts graph substructures into LLM-ready context windows.

    Responsibilities:
    - subgraph compression
    - structured prompt assembly
    - semantic flattening
    """

    def __init__(self):
        pass

    # =====================================================
    # MAIN ENTRY
    # =====================================================

    def build_context(
        self,
        subgraph: GraphSubgraphV2,
        ranked_nodes: Optional[List[str]] = None,
    ) -> Dict[str, object]:

        nodes = subgraph.nodes
        edges = subgraph.edges

        # -------------------------------------------------
        # STEP 1: NODE SERIALIZATION
        # -------------------------------------------------

        node_block = self._serialize_nodes(nodes)

        # -------------------------------------------------
        # STEP 2: EDGE SERIALIZATION
        # -------------------------------------------------

        edge_block = self._serialize_edges(edges)

        # -------------------------------------------------
        # STEP 3: CONTEXT COMPRESSION
        # -------------------------------------------------

        compressed = self._compress_context(node_block, edge_block)

        # -------------------------------------------------
        # FINAL PROMPT STRUCTURE
        # -------------------------------------------------

        return {
            "nodes": node_block,
            "edges": edge_block,
            "compressed_context": compressed,
            "ranked_nodes": ranked_nodes or [],
        }

    # =====================================================
    # NODE SERIALIZATION
    # =====================================================

    def _serialize_nodes(self, nodes):

        return [
            {
                "id": n.id,
                "name": n.name,
                "type": n.type,
                "canonical": n.canonical,
            }
            for n in nodes
        ]

    # =====================================================
    # EDGE SERIALIZATION
    # =====================================================

    def _serialize_edges(self, edges):

        return [
            {
                "id": e.id,
                "source": e.source,
                "target": e.target,
                "type": e.type,
                "layer": e.layer,
                "dispatch": getattr(e, "dispatch", None),
            }
            for e in edges
        ]

    # =====================================================
    # COMPRESSION
    # =====================================================

    def _compress_context(
        self,
        nodes,
        edges,
    ) -> str:

        lines = []

        lines.append("=== GRAPH CONTEXT ===")

        lines.append("\n[NODES]")
        for n in nodes:
            lines.append(f"- {n['name']} ({n['type']})")

        lines.append("\n[EDGES]")
        for e in edges:
            lines.append(f"- {e['source']} -> {e['target']} ({e['type']})")

        return "\n".join(lines)
