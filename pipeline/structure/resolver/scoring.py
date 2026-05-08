# pipeline/structure/resolver/scoring.py


class ResolutionScorer:

    def score(self, candidate, call_name, context):

        score = 0.0

        # match exato de nome
        if candidate.name == call_name:
            score += 0.5

        # mesmo módulo
        if candidate.module_name == context.module:
            score += 0.2

        # mesma classe
        if candidate.parent_symbol_id == context.class_name:
            score += 0.2

        # semântica bônus
        if getattr(candidate, "semantic_type", None) in [
            "mutation",
            "authorization"
        ]:
            score += 0.1

        return score