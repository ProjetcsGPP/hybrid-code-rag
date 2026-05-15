# pipeline/structure/relationship_extractor.py

from pipeline.contracts import Relationship, Symbol
from pipeline.structure.models.semantic_reference import SemanticReference
from pipeline.structure.resolver.call_normalizer import CallNormalizer


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
        references = []

        # -----------------------------------------------------
        # BELONGS_TO
        # -----------------------------------------------------

        if symbol.parent_symbol_id:

            relationships.append(
                Relationship(
                    relationship_id=(
                        f"belongs_to::"
                        f"{symbol.symbol_id}::"
                        f"{symbol.parent_symbol_id}"
                    ),
                    source_symbol_id=symbol.symbol_id,
                    target_symbol_id=symbol.parent_symbol_id,
                    relationship_type="BELONGS_TO",
                )
            )

        # -----------------------------------------------------
        # CALLS
        # -----------------------------------------------------

        for raw_call in symbol.calls:

            callsite = self.normalizer.build_callsite(raw_call)

            # -------------------------------------------------
            # IGNORA BUILTINS
            # -------------------------------------------------

            if callsite.method in self.BUILTIN_METHODS:
                continue

            # -------------------------------------------------
            # SELF METHOD
            # -------------------------------------------------

            if callsite.call_type in ("self_method", "super_method"):

                if callsite.call_type == "super_method":
                    target = self._resolve_super_method(symbol, callsite.method)
                else:
                    target = self._resolve_self_method(symbol, callsite.method)
                if target:

                    if target.symbol_id != symbol.symbol_id:

                        relationships.append(
                            Relationship(
                                relationship_id=(
                                    f"calls_internal::"
                                    f"{symbol.symbol_id}::"
                                    f"{target.symbol_id}"
                                ),
                                source_symbol_id=symbol.symbol_id,
                                target_symbol_id=target.symbol_id,
                                relationship_type="CALLS_INTERNAL",
                                confidence=1.0,
                            )
                        )

                continue

            # -------------------------------------------------
            # LOCAL MODULE FUNCTION
            # -------------------------------------------------

            local_function = self._resolve_local_function(
                symbol,
                callsite.method,
            )

            if local_function:

                if local_function.symbol_id != symbol.symbol_id:

                    relationships.append(
                        Relationship(
                            relationship_id=(
                                f"calls_function::"
                                f"{symbol.symbol_id}::"
                                f"{local_function.symbol_id}"
                            ),
                            source_symbol_id=symbol.symbol_id,
                            target_symbol_id=local_function.symbol_id,
                            relationship_type="CALLS_FUNCTION",
                            confidence=0.9,
                        )
                    )

                continue

            # -------------------------------------------------
            # EXTERNAL / FRAMEWORK / STDLIB
            # -------------------------------------------------

            references.append(
                self._build_reference(
                    symbol,
                    callsite,
                )
            )

        return relationships, references

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

    # ---------------------------------------------------------
    # SEMANTIC REFERENCES
    # ---------------------------------------------------------
    def _build_reference(
        self,
        symbol,
        callsite,
    ):

        ref_type = "EXTERNAL_REFERENCE"

        if callsite.call_type == "self_method":
            ref_type = "INTERNAL_REFERENCE"

        elif callsite.call_type == "super_method":
            ref_type = "SUPER_REFERENCE"

        elif callsite.owner in self.BUILTIN_OWNERS:
            ref_type = "BUILTIN_REFERENCE"

        elif callsite.owner in self.STDLIB_OWNERS:
            ref_type = "STDLIB_REFERENCE"

        elif callsite.owner == "models":
            ref_type = "FRAMEWORK_REFERENCE"

        return SemanticReference(
            reference_id=(f"semantic_ref::" f"{symbol.symbol_id}::" f"{callsite.raw}"),
            source_symbol_id=symbol.symbol_id,
            reference_type=ref_type,
            raw_call=callsite.raw,
            owner=callsite.owner,
            method=callsite.method,
            confidence=0.5,
        )
