# pipeline/structure/semantic/semantic_reference_builder.py

from pipeline.structure.models.semantic_reference import SemanticReference


class SemanticReferenceBuilder:

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

    FRAMEWORK_MODULE_HINTS = {
        "django": "DJANGO",
        "rest_framework": "DRF",
        "fastapi": "FASTAPI",
        "sqlalchemy": "SQLALCHEMY",
    }

    def build(
        self,
        symbol,
        symbol_index,
        variable_registry=None,
    ):

        references = []

        raw_calls = symbol.calls or []

        imports = symbol.imports or []

        import_lookup = self._build_import_lookup(imports)

        for raw_call in raw_calls:

            owner, method = self._split_call(raw_call)

            binding = self._resolve_variable_binding(
                owner,
                variable_registry,
            )

            reference_type = self._infer_reference_type(
                owner,
                method,
                raw_call,
                import_lookup,
                binding,
            )

            resolved_to = self._resolve_reference(
                owner,
                method,
                import_lookup,
                binding,
            )

            framework_hint = self._infer_framework_hint(
                resolved_to,
                owner,
            )

            module_name = self._extract_module_name(
                resolved_to,
            )

            references.append(
                SemanticReference(
                    reference_id=(f"ref::" f"{symbol.symbol_id}::" f"{raw_call}"),
                    source_symbol_id=symbol.symbol_id,
                    reference_type=reference_type,
                    raw_call=raw_call,
                    owner=owner,
                    method=method,
                    resolved_to=resolved_to,
                    module_name=module_name,
                    framework_hint=framework_hint,
                    confidence=self._confidence_for(reference_type),
                    metadata={
                        "resolver": "SemanticReferenceBuilder",
                    },
                )
            )

        return references

    # ---------------------------------------------------------
    # IMPORT LOOKUP
    # ---------------------------------------------------------

    def _build_import_lookup(self, imports):

        lookup = {}

        for imp in imports:

            local_name = imp.get("local_name")
            module = imp.get("module")
            imported = imp.get("imported")

            if imported:

                full_path = f"{module}.{imported}"

            else:

                full_path = module

            lookup[local_name] = {
                "module": module,
                "imported": imported,
                "full_path": full_path,
            }

        return lookup

    # ---------------------------------------------------------
    # CALL PARSER
    # ---------------------------------------------------------

    def _split_call(self, raw_call):

        if "." not in raw_call:
            return raw_call, None

        parts = raw_call.split(".")

        owner = ".".join(parts[:-1])

        method = parts[-1]

        return owner, method

    # ---------------------------------------------------------
    # TYPE INFERENCE
    # ---------------------------------------------------------

    def _infer_reference_type(
        self,
        owner,
        method,
        raw_call,
        import_lookup,
        binding=None,
    ):

        if owner in import_lookup:
            return "IMPORTED_SYMBOL"

        if owner in self.STDLIB_OWNERS:
            return "STDLIB"

        if owner in self.BUILTIN_OWNERS:
            return "BUILTIN"

        if binding:

            # ---------------------------------------------
            # QuerySet propagation
            # ---------------------------------------------

            if binding.semantic_type == "queryset":

                if binding.model_name and method:

                    return f"{binding.model_name}" f".queryset.{method}"

            # ---------------------------------------------
            # ORM manager propagation
            # ---------------------------------------------

            if binding.semantic_type == "manager":

                if binding.model_name and method:

                    return f"{binding.model_name}" f".objects.{method}"

            # ---------------------------------------------
            # Model instance propagation
            # ---------------------------------------------

            if binding.semantic_type == "model_instance":

                if binding.model_name and method:

                    return f"{binding.model_name}.{method}"

        if owner and owner.endswith(".objects"):
            return "ORM_MANAGER"

        if owner and owner.startswith("self.") and method in self.BUILTIN_METHODS:
            return "INSTANCE_ATTRIBUTE_METHOD"

        if method in self.BUILTIN_METHODS:
            return "RUNTIME_METHOD"

        if owner == "self":
            return "SELF_REFERENCE"

        if owner == "super":
            return "SUPER_REFERENCE"

        if raw_call.endswith("Error"):
            return "EXCEPTION"

        return "EXTERNAL"

    # ---------------------------------------------------------
    # RESOLUTION
    # ---------------------------------------------------------

    def _resolve_reference(
        self,
        owner,
        method,
        import_lookup,
        binding=None,
    ):

        if binding:

            if binding.semantic_type == "queryset":

                if binding.model_name and method:
                    return f"{binding.model_name}" f".queryset.{method}"

            if binding.semantic_type == "manager":

                if binding.model_name and method:
                    return f"{binding.model_name}" f".objects.{method}"

            if binding.semantic_type == "model_instance":

                if binding.model_name and method:
                    return f"{binding.model_name}.{method}"

        if owner in import_lookup:

            resolved = import_lookup[owner]["full_path"]

            if method:
                return f"{resolved}.{method}"

            return resolved

        if owner and method:
            return f"{owner}.{method}"

        return owner

    # ---------------------------------------------------------
    # FRAMEWORK INFERENCE
    # ---------------------------------------------------------

    def _infer_framework_hint(
        self,
        resolved_to,
        owner,
    ):

        target = resolved_to or owner or ""

        for prefix, framework in self.FRAMEWORK_MODULE_HINTS.items():

            if target.startswith(prefix):
                return framework

        if owner in self.STDLIB_OWNERS:
            return "STDLIB"

        if owner in self.BUILTIN_OWNERS:
            return "BUILTIN"

        return None

    # ---------------------------------------------------------
    # MODULE EXTRACTION
    # ---------------------------------------------------------

    def _extract_module_name(
        self,
        resolved_to,
    ):

        if not resolved_to:
            return None

        parts = resolved_to.split(".")

        if len(parts) <= 1:
            return resolved_to

        return ".".join(parts[:-1])

    # ---------------------------------------------------------
    # CONFIDENCE
    # ---------------------------------------------------------

    def _confidence_for(
        self,
        reference_type,
    ):

        mapping = {
            "IMPORTED_SYMBOL": 1.0,
            "STDLIB": 1.0,
            "BUILTIN": 1.0,
            "ORM_MANAGER": 0.95,
            "SELF_REFERENCE": 0.9,
            "SUPER_REFERENCE": 0.9,
            "RUNTIME_METHOD": 0.5,
            "EXCEPTION": 0.9,
            "EXTERNAL": 0.7,
            "QUERYSET_METHOD": 0.92,
            "MODEL_METHOD": 0.90,
            "INSTANCE_ATTRIBUTE_METHOD": 0.6,
        }

        return mapping.get(reference_type, 0.5)

    def _resolve_variable_binding(
        self,
        owner,
        variable_registry,
    ):

        if not variable_registry:
            return None

        return variable_registry.get(owner)
