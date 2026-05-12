#  pipeline/structure/context/assembly_engine.py

from pipeline.structure.structural_query import StructuralQuery


class ContextAssemblyEngine:

    def __init__(self, query: StructuralQuery):
        self.query = query

    def build(self, symbol_id: str):
        symbol = self.query.get_symbol(symbol_id)

        children = self.query.get_children(symbol_id)
        relationships = self.query.get_relationships(symbol_id)

        siblings = self._get_siblings(symbol_id)

        return {
            "symbol": symbol,
            "children": children,
            "relationships": relationships,
            "siblings": siblings
        }

    def _get_siblings(self, symbol_id: str):
        parent = self.query.get_parent(symbol_id)
        if not parent:
            return []

        return self.query.get_children(parent["id"])