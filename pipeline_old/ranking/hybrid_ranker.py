from pipeline.intent.intent_classifier import detect_intent
import unicodedata


def normalize(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text.lower())
    return text.encode("ascii", "ignore").decode("utf-8")


class HybridRanker:

    def rank(self, query, results):

        intent = detect_intent(query)

        query_norm = normalize(query)

        ranked = []

        for r in results:

            meta = r["meta"]

            name = normalize(meta.get("name", ""))

            # -----------------------------
            # 1. SCORES BASE
            # -----------------------------
            vector_score = float(r.get("vector_score", 0.0))
            semantic_score = float(r.get("semantic_score", 0.0))
            importance_score = float(meta.get("importance_score", 1.0))

            # -----------------------------
            # 2. STRUCTURAL SCORE (determinístico)
            # -----------------------------
            structural_score = 0.0

            if "clean" in name or "validate" in name:
                structural_score = 0.7
            elif "save" in name or "create" in name:
                structural_score = 0.5
            elif meta.get("type") == "class":
                structural_score = 0.4

            # -----------------------------
            # 3. INTENT SCORE (substitui boost antigo)
            # -----------------------------
            intent_score = 0.0

            semantic_type = meta.get("semantic_type", "")

            if intent == "validation_search" and "validation" in semantic_type:
                intent_score = 1.0

            elif intent == "mutation_search" and semantic_type == "mutation":
                intent_score = 1.0

            elif intent == "auth_search" and semantic_type == "authorization":
                intent_score = 1.0

            elif intent == "code_location_search":
                intent_score = 0.6

            # -----------------------------
            # 4. IMPORTANCE NORMALIZATION
            # -----------------------------
            norm_importance = min(importance_score / 2.0, 1.0)

            # -----------------------------
            # 5. FINAL SCORE (FUNÇÃO FIXA)
            # -----------------------------
            final_score = (
                vector_score * 0.40 +
                semantic_score * 0.25 +
                structural_score * 0.15 +
                norm_importance * 0.10 +
                intent_score * 0.10
            )

            ranked.append({
                "doc": r["doc"],
                "meta": meta,

                "vector_score": vector_score,
                "semantic_score": semantic_score,
                "structural_score": structural_score,
                "importance_score": importance_score,
                "intent_score": intent_score,

                "final_score": final_score,
            })

        return sorted(ranked, key=lambda x: x["final_score"], reverse=True)