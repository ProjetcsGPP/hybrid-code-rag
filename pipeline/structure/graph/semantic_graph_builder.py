# pipeline/structure/graph/semantic_graph_builder.py

from pipeline.structure.resolver.call_normalizer import CallNormalizer
from pipeline.contracts import Relationship


class SemanticGraphBuilder:

    def __init__(self, graph_store, semantic_resolver):

        self.graph = graph_store
        self.resolver = semantic_resolver
        self.normalizer = CallNormalizer()

    def build_edges(self, symbol):

        edges = []

        for raw_call in symbol.calls:

            # ---------------------------------
            # NORMALIZE FIRST
            # ---------------------------------

            normalized = self.normalizer.normalize(
                raw_call,
                symbol
            )

            if not normalized:
                continue

            # ---------------------------------
            # BUILD CALLSITE
            # ---------------------------------

            callsite = self.normalizer.build_callsite(
                normalized
            )

            semantic = self.resolver.resolve(
                callsite,
                symbol
            )

            target = semantic["target"]

            # ---------------------------------
            # TARGET REAL
            # ---------------------------------

            if target:

                target_id = target.symbol_id

            # ---------------------------------
            # EXTERNAL NODE
            # ---------------------------------

            else:

                target_id = self.graph.ensure_external_node(
                    owner=callsite.owner,
                    name=callsite.method
                )

            # ---------------------------------
            # EDGE
            # ---------------------------------

            edge = Relationship(

                relationship_id=(
                    f"calls::{symbol.symbol_id}::"
                    f"{callsite.raw}::"
                    f"{semantic['type']}"
                ),

                source_symbol_id=symbol.symbol_id,

                target_symbol_id=target_id,

                relationship_type=(
                    f"CALLS::{semantic['type']}"
                ),

                confidence=semantic["confidence"],
            )

            edges.append(edge)

        return edges