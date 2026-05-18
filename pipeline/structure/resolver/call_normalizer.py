# pipeline/structure/resolver/call_normalizer.py

from pipeline.structure.models.callsite import CallSite


class CallNormalizer:

    INVALID_NAMESPACE_PREFIXES = (
        "models.",
        "django.",
    )

    INVALID_RUNTIME_CONTAINS = (
        ".objects.",
        ".filter",
        ".exclude",
        ".exists",
        ".all",
    )

    INVALID_CALL_PREFIXES = ("ValidationError",)

    DJANGO_FIELDS = (
        "CharField",
        "ForeignKey",
        "OneToOneField",
        "DateTimeField",
        "BigIntegerField",
        "IntegerField",
        "BooleanField",
        "TextField",
        "URLField",
        "AutoField",
        "SmallIntegerField",
        "GenericIPAddressField",
        "Index",
        "UniqueConstraint",
    )

    def normalize(self, call: str, context_symbol=None):

        if not call:
            return None

        # ----------------------------
        # BLOCK 1: namespace noise
        # ----------------------------
        if any(call.startswith(p) for p in self.INVALID_NAMESPACE_PREFIXES):
            return None

        # ----------------------------
        # BLOCK 2: runtime ORM noise
        # ----------------------------
        if any(x in call for x in self.INVALID_RUNTIME_CONTAINS):
            return None

        # ----------------------------
        # BLOCK 3: django fields / constructs
        # ----------------------------
        if any(f in call for f in self.DJANGO_FIELDS):
            return None

        # ----------------------------
        # BLOCK 4: direct invalid calls
        # ----------------------------
        if any(call.startswith(p) for p in self.INVALID_CALL_PREFIXES):
            return None

        # ----------------------------
        # self.method → Class.method
        # ----------------------------
        if call.startswith("self."):
            return call

        # ----------------------------
        # super.method → method
        # ----------------------------

        if call == "super":
            return None

        if call.startswith("super."):
            return call

        return call

    # ---------------------------------------------------------
    # CALLSITE
    # ---------------------------------------------------------

    def build_callsite(self, raw: str):

        parts = raw.split(".")
        calltype = "unknown"

        # -----------------------------------------
        # function()
        # -----------------------------------------

        if len(parts) == 1:

            calltype = "function"

            return CallSite(
                raw=raw,
                owner=None,
                method=parts[0],
                chain=[],
                normalized=raw,
                call_type=calltype,
            )

        # -----------------------------------------
        # self.method()
        # -----------------------------------------

        if parts[0] == "self":

            # self.save()
            if len(parts) == 2:
                calltype = "self_method"

            # self.attr.method()
            else:
                calltype = "attribute_method"

            return CallSite(
                raw=raw,
                owner="self",
                method=parts[-1],
                chain=parts[1:-1],
                normalized=f"self.{parts[-1]}",
                call_type=calltype,
            )

        # -----------------------------------------
        # super.method()
        # -----------------------------------------

        if parts[0] == "super":

            calltype = "super_method"

            return CallSite(
                raw=raw,
                owner="super",
                method=parts[-1],
                chain=parts[1:-1],
                normalized=f"super.{parts[-1]}",
                call_type=calltype,
            )

        # -----------------------------------------
        # generic owner.method()
        # -----------------------------------------
        calltype = "method"

        return CallSite(
            raw=raw,
            owner=parts[0],
            method=parts[-1],
            chain=parts[1:-1],
            normalized=f"{parts[0]}.{parts[-1]}",
            call_type=calltype,
        )
