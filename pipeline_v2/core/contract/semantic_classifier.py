# pipeline_v2/core/contract/semantic_classifier.py

from pipeline_v2.core.relationship.relationship_types import (
    RelationshipType,
)


class SemanticCallClassifier:

    VALID_DISPATCHES = {
        "SELF",
        "SUPER",
        "ORM",
        "FRAMEWORK",
        "DIRECT",
        "INSTANCE",
        "CHAIN",
    }

    @classmethod
    def validate_dispatch(cls, dispatch: str):

        if dispatch not in cls.VALID_DISPATCHES:
            raise ValueError(f"Unknown dispatch: {dispatch}")

        return dispatch

    @staticmethod
    def classify(call: str):
        """
        Classificação única e global de chamadas semânticas.
        REGRA: nenhuma outra camada pode redefinir isso.
        """

        if call.startswith("self."):
            return RelationshipType.SELF_CALL, "SELF"

        if call.startswith("super."):
            return RelationshipType.SUPER_CALL, "SUPER"

        if "objects." in call:
            return RelationshipType.ORM_QUERY, "ORM"

        if "." in call:
            return RelationshipType.FRAMEWORK_CALL, "FRAMEWORK"

        return RelationshipType.CALLS, "DIRECT"
