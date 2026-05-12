# pipeline/structure/resolver/call_normalizer.py

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

    INVALID_CALL_PREFIXES = (
        "ValidationError",
    )

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