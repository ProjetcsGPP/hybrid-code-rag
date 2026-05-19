# pipeline/structure/relationship_extractor.py

from pipeline.contracts import Relationship, Symbol
from pipeline.structure.resolver.call_normalizer import CallNormalizer
from pipeline.structure.semantic.relationship_semantic_mapper import (
    RelationshipSemanticMapper,
)


class RelationshipExtractor:

    BUILTIN_METHODS = {
        "upper",
        "lower",
        "strip",
        "split",
        "join",
        "replace",
        "format",
        "exists",
        "exclude",
        "filter",
        "all",
        "first",
        "last",
        "count",
    }

    BUILTIN_OWNERS = {
        "str",
        "int",
        "float",
        "dict",
        "list",
        "set",
        "tuple",
    }

    STDLIB_OWNERS = {
        "datetime",
        "json",
        "pathlib",
        "os",
        "re",
        "typing",
        "timezone",
    }

    def __init__(self, symbol_index):

        self.normalizer = CallNormalizer()

        print("\nREL EXTRACTOR INIT")
        print("SYMBOL INDEX ID:", id(symbol_index))

        self.symbol_index = symbol_index
        if self.symbol_index is None:
            raise ValueError("SymbolIndex must be provided " "(no fallback allowed)")

    # ---------------------------------------------------------
    # PUBLIC
    # ---------------------------------------------------------

    def extract(
        self,
        symbol: Symbol,
        symbol_index,
        resolver,
    ):

        relationships = []

        # -----------------------------------------------------
        # BELONGS_TO
        # -----------------------------------------------------

        if symbol.parent_symbol_id:

            rel = Relationship(
                relationship_id=(
                    f"belongs_to::" f"{symbol.symbol_id}::" f"{symbol.parent_symbol_id}"
                ),
                source_symbol_id=symbol.symbol_id,
                target_symbol_id=symbol.parent_symbol_id,
                relationship_type="BELONGS_TO",
            )

            RelationshipSemanticMapper.enrich(
                rel,
                resolved=True,
            )

            relationships.append(rel)

        return relationships

    # ---------------------------------------------------------
    # SELF METHODS
    # ---------------------------------------------------------

    def _resolve_self_method(
        self,
        context_symbol,
        method_name,
    ):

        print("SELF METHOD RESOLVE:")
        print("CONTEXT:", context_symbol.symbol_id)
        print("PARENT:", context_symbol.parent_symbol_id)
        print("SEARCH:", method_name)
        print("CURRENT INDEX ID:", id(self.symbol_index))

        if not context_symbol.parent_symbol_id:
            return None

        # 🔥 USA RESOLVER DE HIERARQUIA (FONTE ÚNICA)
        target = self.symbol_index.find_method_in_hierarchy(
            context_symbol.parent_symbol_id,
            method_name,
        )

        print("RETURNED IN _resolve_self_method TARGET:", target)

        return target

    def _resolve_super_method(self, context_symbol, method_name):

        if not context_symbol.parent_symbol_id:
            return None

        # por enquanto: fallback simples
        # TODO: depois mapear MRO corretamente

        # class_symbols = self.symbol_index.get_class_symbols(
        #     context_symbol.parent_symbol_id
        # )
        #
        # for symbol in class_symbols:
        #     if symbol.name == method_name:
        #         return symbol

        target = self.symbol_index.find_method_in_hierarchy(
            context_symbol.parent_symbol_id,
            method_name,
        )
        print("RETURNED IN _resolve_super_method TARGET:", target)

        return target

    # ---------------------------------------------------------
    # LOCAL FUNCTIONS
    # ---------------------------------------------------------
    def _resolve_local_function(
        self,
        context_symbol,
        function_name,
    ):

        return self.symbol_index.find_local_function(
            context_symbol.module_name,
            function_name,
        )
