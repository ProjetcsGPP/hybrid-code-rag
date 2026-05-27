# pipeline_v2/core/state/assignment_resolver.py

from pipeline_v2.core.state.variable_state import VariableState


class AssignmentResolverV2:
    """
    Resolve assignments AST em estado semântico transitório.

    NÃO resolve:
    - symbol graph
    - runtime graph
    - imports globais

    Atua apenas localmente.
    """

    BUILTIN_INSTANCE_HINTS = {
        "Repository",
        "Connection",
        "Service",
        "Client",
        "Manager",
        "Controller",
    }

    ORM_QUERYSET_HINTS = {
        "objects.filter",
        "objects.exclude",
        "objects.get",
        "objects.create",
    }

    def resolve(self, assignment: dict):

        variable = assignment.get("variable")

        if not variable:
            return None

        source = assignment.get("source")

        semantic_type = assignment.get(
            "semantic_type",
            "unknown",
        )

        model = assignment.get("model")

        confidence = assignment.get(
            "confidence",
            0.50,
        )

        framework_hint = assignment.get(
            "framework_hint",
        )

        # ---------------------------------------------------------
        # INSTANCE CONSTRUCTOR INFERENCE
        # ---------------------------------------------------------

        inferred = self._infer_instance_type(source)

        if inferred:

            semantic_type = "instance"

            model = source

            confidence = max(confidence, 0.85)

        # ---------------------------------------------------------
        # QUERYSET INFERENCE
        # ---------------------------------------------------------

        queryset_model = self._infer_queryset_model(source)

        if queryset_model:

            semantic_type = "queryset"

            model = queryset_model

            framework_hint = "django"

            confidence = max(confidence, 0.90)

        return VariableState(
            name=variable,
            source=source,
            semantic_type=semantic_type,
            model=model,
            confidence=confidence,
            framework_hint=framework_hint,
            provenance="SEMANTIC_ASSIGNMENT_RESOLUTION",
        )

    # =========================================================
    # INSTANCE INFERENCE
    # =========================================================

    def _infer_instance_type(self, source):

        if not source:
            return False

        if "." in source:
            return False

        for hint in self.BUILTIN_INSTANCE_HINTS:

            if source.endswith(hint):
                return True

        if source[:1].isupper():
            return True

        return False

    # =========================================================
    # QUERYSET INFERENCE
    # =========================================================

    def _infer_queryset_model(self, source):

        if not source:
            return None

        for hint in self.ORM_QUERYSET_HINTS:

            if hint in source:

                model = source.split(".")[0]

                return model

        return None
