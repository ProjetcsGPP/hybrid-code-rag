# pipeline/structure/resolver/semantic_call_resolver.py

from pipeline.structure.resolver.semantic_call import SemanticCallTarget
from pipeline.structure.models.callsite import CallSite
from pipeline.contracts import Symbol


class SemanticCallResolver:

    def __init__(self, symbol_index):
        self.index = symbol_index

    # -----------------------------
    # ENTRYPOINT
    # -----------------------------
    def resolve(
        self,
        call: CallSite,
        context: Symbol
    ) -> SemanticCallTarget:

        # -------------------------
        # SELF CALL
        # -------------------------
        if call.call_type == "self_method":

            target = self._resolve_self_method(
                call,
                context,
            )

            return SemanticCallTarget(
                raw=call.raw,
                owner_name=context.name if context else None,
                method=call.method,
                call_type="SELF_METHOD",
                resolved_symbol=target,
                confidence=0.95 if target else 0.0,
            )

        # -------------------------
        # SUPER CALL
        # -------------------------
        if call.call_type == "super_method":

            return SemanticCallTarget(
                raw=call.raw,
                owner_name=context.name if context else None,
                method=call.method,
                call_type="SUPER_METHOD",
                resolved_symbol=None,
                confidence=0.0,
            )


        # -------------------------
        # ORM / DOTTED CALL
        # -------------------------
        if call.owner:

            owner_symbol = self.index.resolve_best(call.owner, context)

            if owner_symbol:

                # ORM DETECTION (objects.manager pattern)
                if "objects" in call.chain:

                    return SemanticCallTarget(
                        raw=call.raw,
                        owner_name=owner_symbol.name,
                        method=call.method,
                        call_type="ORM_MANAGER",
                        resolved_symbol=self._resolve_in_symbol(owner_symbol, call.method),
                        confidence=0.95
                    )

                return SemanticCallTarget(
                    raw=call.raw,
                    owner_name=owner_symbol.name,
                    method=call.method,
                    call_type="METHOD",
                    resolved_symbol=self._resolve_in_symbol(owner_symbol, call.method),
                    confidence=0.8
                )

        # -------------------------
        # FUNCTION CALL
        # -------------------------
        candidates = self.index.by_name.get(call.method, [])

        if candidates:

            return SemanticCallTarget(
                raw=call.raw,
                owner_name=None,
                method=call.method,
                call_type="FUNCTION",
                resolved_symbol=candidates[0],
                confidence=0.6
            )

        # -------------------------
        # FALLBACK EXTERNAL
        # -------------------------
        return SemanticCallTarget(
            raw=call.raw,
            owner_name=call.owner,
            method=call.method,
            call_type="EXTERNAL",
            resolved_symbol=None,
            confidence=0.0
        )

    # -----------------------------
    # HELPERS
    # -----------------------------

    def _resolve_self_method(
        self,
        callsite,
        context_symbol,
    ):
        """
        Resolve chamadas self.metodo()
        dentro da própria classe.
        """

        if not context_symbol.parent_symbol_id:
            return None

        parent_class_id = context_symbol.parent_symbol_id

        candidates = self.index.search(callsite.method)

        for c in candidates:

            if c.parent_symbol_id == parent_class_id:
                return c

        return None


    def _resolve_in_class(self, context, method_name):

        if not context:
            return None

        if not context.parent_symbol_id:
            return None

        class_methods = self.index.get_class_symbols(
            context.parent_symbol_id
        )

        for method in class_methods:

            if method.name == method_name:
                return method

        return None

    def _resolve_parent(self, context):
        if not context or not context.parent_symbol_id:
            return None

        return self.index.get(context.parent_symbol_id)

    def _resolve_in_symbol(self, symbol, method_name):
        if not symbol:
            return None

        return self.index.resolve_best(method_name, symbol)