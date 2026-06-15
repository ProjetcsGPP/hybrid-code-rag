# pipeline_v2/core/state/assignment_resolver.py


from pipeline_v2.core.state.variable_state import VariableState
from pipeline_v2.core.contract.contract_enforcer import (
    ContractEnforcer,
)


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

    def resolve(self, assignment):

        assignment = ContractEnforcer.enforce_assignment(assignment)

        variable = assignment.variable
        if not variable:
            return None

        source = assignment.source
        if not source:
            return None

        semantic_type = assignment.semantic_type
        model = assignment.model
        confidence = assignment.confidence
        framework_hint = assignment.framework_hint

        # =========================================================
        # INSTANCE INFERENCE (PRIORIDADE ALTA)
        # =========================================================
        if self._is_instance(source):
            semantic_type = "instance"
            model = source
            confidence = max(confidence, 0.85)

        # =========================================================
        # QUERYSET INFERENCE (OVERRIDES INSTANCE SE DETECTADO)
        # =========================================================
        queryset_model = self._infer_queryset_model(source)
        if queryset_model:
            semantic_type = "queryset"
            model = queryset_model
            framework_hint = "django"
            confidence = max(confidence, 0.90)

        # =========================================================
        # NORMALIZAÇÃO FINAL DE CONSISTÊNCIA
        # =========================================================
        semantic_type = self._normalize_semantic_type(semantic_type)

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
    # INSTANCE DETECTION
    # =========================================================
    def _is_instance(self, source: str) -> bool:

        if not source:
            return False

        if "." in source:
            return False

        return source[:1].isupper() or any(
            source.endswith(h) for h in self.BUILTIN_INSTANCE_HINTS
        )

    # =========================================================
    # QUERYSET DETECTION
    # =========================================================
    def _infer_queryset_model(self, source: str):

        if not source:
            return None

        for hint in self.ORM_QUERYSET_HINTS:
            if hint in source:
                return source.split(".")[0]

        return None

    # =========================================================
    # NORMALIZAÇÃO SEMÂNTICA (CRÍTICO)
    # =========================================================
    def _normalize_semantic_type(self, semantic_type: str) -> str:

        valid = {
            "instance",
            "queryset",
            "attribute_chain",
            "unknown",
        }

        return semantic_type if semantic_type in valid else "unknown"
