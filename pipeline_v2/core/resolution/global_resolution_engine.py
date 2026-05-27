# pipeline_v2/core/resolution/global_resolution_engine.py


class GlobalResolutionEngineV2:

    def __init__(
        self,
        identity_registry,
        graph_index=None,
    ):

        self.identity_registry = identity_registry

        self.graph_index = graph_index

    # =====================================================
    # SYMBOL
    # =====================================================

    def resolve_symbol(self, name):

        matches = self.identity_registry.resolve_by_name(name)

        if matches:
            return matches[0]

        return None

    # =====================================================
    # CANONICAL
    # =====================================================

    def resolve_canonical(self, canonical):

        return self.identity_registry.resolve_by_canonical(canonical)

    # =====================================================
    # TARGET
    # =====================================================

    def resolve_target(self, raw_call):

        # exact canonical
        exact = self.resolve_canonical(raw_call)

        if exact:
            return exact.id

        # name match
        symbol = self.resolve_symbol(raw_call)

        if symbol:
            return symbol.id

        return f"UNRESOLVED::{raw_call}"
