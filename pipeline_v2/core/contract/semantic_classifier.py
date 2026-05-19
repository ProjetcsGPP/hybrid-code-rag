# pipeline_v2/core/contract/semantic_classifier.py


class SemanticCallClassifier:

    @staticmethod
    def classify(call: str):
        """
        Classificação única e global de chamadas semânticas.
        REGRA: nenhuma outra camada pode redefinir isso.
        """

        if call.startswith("self."):
            return "SELF_CALL", "SELF"

        if call.startswith("super."):
            return "SUPER_CALL", "SUPER"

        if "objects." in call:
            return "ORM_QUERY", "ORM"

        # padrão framework / dotted calls
        if "." in call:
            return "FRAMEWORK_CALL", "FRAMEWORK"

        return "CALLS", "DIRECT"
