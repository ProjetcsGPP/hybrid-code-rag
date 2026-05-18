# pipeline/structure/resolver/call_resolver.py

from pipeline.structure.models.callsite import CallSite
from pipeline.structure.resolver.symbol_index import SymbolIndex
from pipeline.contracts import Symbol


class CallResolver:

    def __init__(self, index: SymbolIndex):

        self.index = index

    # -------------------------------------------------
    # PUBLIC
    # -------------------------------------------------

    def resolve(
        self,
        call: CallSite,
        context: Symbol,
        variable_registry=None,
    ):

        # ---------------------------------------------
        # self.method()
        # ---------------------------------------------

        if call.call_type == "self_method":

            target = self.index.find_method_in_hierarchy(
                context.parent_symbol_id,
                call.method,
            )

            # 🔥 FRAMEWORK ENHANCEMENT (Django fix)
            if not target:
                print(
                    "CALL RESOLVER: resolve(self_method) TARGET NONE FOR SYMBOL:",
                    context.symbol_id,
                )
                target = self.index.resolve_framework_method(
                    "models.Model",
                    call.method,
                )

            return {
                "type": (
                    "SELF"
                    if target and (target.parent_symbol_id == context.parent_symbol_id)
                    else "INHERITED"
                ),
                "target": target,
                "confidence": (1.0 if target and target.symbol_id else 0.0),
            }

        # ---------------------------------------------
        # self.attr.method()
        # ---------------------------------------------

        if call.call_type == "attribute_method":

            binding = None

            if variable_registry:
                binding = variable_registry.get(call.owner)

            # -----------------------------------------
            # QUERYSET
            # -----------------------------------------

            if binding and binding.semantic_type == "queryset":

                return {
                    "type": "QUERYSET",
                    "target": None,
                    "confidence": binding.confidence,
                    "framework": "DJANGO",
                }

            # -----------------------------------------
            # MODEL INSTANCE
            # -----------------------------------------

            if binding and binding.semantic_type == "model_instance":

                class_symbol = self.index.resolve_class_by_name(binding.model_name)

                target = None

                if class_symbol:

                    target = self.index.find_method_in_hierarchy(
                        class_symbol.symbol_id,
                        call.method,
                    )

                return {
                    "type": "MODEL_METHOD",
                    "target": target,
                    "confidence": 0.9 if target else 0.4,
                    "framework": "DJANGO",
                }

            return {
                "type": "RUNTIME",
                "target": None,
                "confidence": 0.3,
            }

        # ---------------------------------------------
        # super().method()
        # ---------------------------------------------

        if call.call_type == "super_method":

            class_id = context.parent_symbol_id

            if not class_id:
                return {
                    "type": "SUPER",
                    "target": None,
                    "confidence": 0.0,
                }

            bases = self.index.inheritance_index.get(class_id, [])

            for base_name in bases:

                # ---------------------------------
                # DJANGO / FRAMEWORK
                # ---------------------------------

                framework = self.index.resolve_framework_method(
                    base_name,
                    call.method,
                )

                if framework:
                    return {
                        "type": "SUPER",
                        "target": framework,
                        "confidence": 1.0,
                    }

                # ---------------------------------
                # LOCAL BASE CLASS
                # ---------------------------------

                base_symbol = self.index.resolve_class_by_name(base_name)

                if not base_symbol:
                    continue

                target = self.index.find_method_in_class(
                    base_symbol.symbol_id,
                    call.method,
                )

                if target:
                    return {
                        "type": "SUPER",
                        "target": target,
                        "confidence": 0.95,
                    }

            return {
                "type": "SUPER",
                "target": None,
                "confidence": 0.3,
            }

        # ---------------------------------------------
        # imported/external symbols
        # ---------------------------------------------

        if call.owner:

            if self._is_imported(
                call.owner,
                context,
            ):

                return {
                    "type": "EXTERNAL",
                    "target": None,
                    "confidence": 0.8,
                }

        # ---------------------------------------------
        # local function()
        # ---------------------------------------------

        target = self.index.find_local_function(
            context.module_name,
            call.method,
        )

        if target:

            return {
                "type": "FUNCTION",
                "target": target,
                "confidence": 0.9,
            }

        # ---------------------------------------------
        # fallback
        # ---------------------------------------------

        return {
            "type": "REFERENCE",
            "target": None,
            "confidence": 0.0,
        }

    # -------------------------------------------------
    # INTERNAL
    # -------------------------------------------------

    def _is_imported(
        self,
        owner_name: str,
        context: Symbol,
    ):

        for imp in context.imports:

            if imp.get("local_name") == owner_name:
                return True

        return False
