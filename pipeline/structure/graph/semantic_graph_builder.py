# pipeline/structure/graph/semantic_graph_builder.py

from pipeline.structure.models.callsite import CallSite


class SemanticGraphBuilder:

    def __init__(self, graph_store, semantic_resolver):

        self.graph = graph_store
        self.resolver = semantic_resolver

    def build_edges(self, symbol):

        edges = []

        for raw_call in symbol.calls:

            callsite = CallSite(raw=raw_call)

            semantic = self.resolver.resolve(callsite, symbol)

            target = semantic.resolved_symbol

            edge = {
                "relationship_id": f"calls::{symbol.symbol_id}::{raw_call}",
                "source_symbol_id": symbol.symbol_id,
                "target_symbol_id": target.symbol_id if target else None,
                "relationship_type": f"CALLS::{semantic.call_type}",
                "confidence": semantic.confidence,
                "raw_call": raw_call
            }

            edges.append(edge)

        return edges