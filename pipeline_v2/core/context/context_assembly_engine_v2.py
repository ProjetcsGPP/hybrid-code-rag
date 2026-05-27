# pipeline_v2/core/context/context_assembly_engine_v2.py


from typing import Dict, List, Any, Optional


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
        subgraph: Dict[str, Any],
        ranked_nodes: Optional[List[str]] = None,
    ) -> Dict[str, Any]:

        nodes = subgraph.get("nodes", [])
        edges = subgraph.get("edges", [])

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

    def _serialize_nodes(self, nodes: List[Any]) -> List[Dict[str, Any]]:

        result = []

        for n in nodes:

            if isinstance(n, dict):
                result.append(
                    {
                        "id": n.get("id"),
                        "name": n.get("name"),
                        "type": n.get("type"),
                        "canonical": n.get("canonical"),
                    }
                )
            else:
                result.append({"id": str(n)})

        return result

    # =====================================================
    # EDGE SERIALIZATION
    # =====================================================

    def _serialize_edges(self, edges: List[Any]) -> List[Dict[str, Any]]:

        result = []

        for e in edges:

            result.append(
                {
                    "id": e.get("id"),
                    "source": e.get("source"),
                    "target": e.get("target"),
                    "type": e.get("type"),
                    "layer": e.get("layer"),
                    "dispatch": e.get("dispatch"),
                }
            )

        return result

    # =====================================================
    # COMPRESSION
    # =====================================================

    def _compress_context(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
    ) -> str:

        lines = []

        lines.append("=== GRAPH CONTEXT ===")

        lines.append("\n[NODES]")
        for n in nodes:
            lines.append(f"- {n.get('name')} ({n.get('type')})")

        lines.append("\n[EDGES]")
        for e in edges:
            lines.append(f"- {e.get('source')} -> {e.get('target')} ({e.get('type')})")

        return "\n".join(lines)
