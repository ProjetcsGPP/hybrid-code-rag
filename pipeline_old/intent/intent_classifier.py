# ==============================
# pipeline/intent/intent_classifier.py
# ==============================

from difflib import SequenceMatcher
from pipeline.intent.intent_registry import INTENT_SEEDS


# ------------------------------
# 1. RULE-BASED FAST PATH
# ------------------------------

def rule_based_intent(query: str):
    q = query.lower()

    # validation
    if any(k in q for k in ["validação", "validate", "validation", "clean", "regra"]):
        return "validation_search"

    # mutation
    if any(k in q for k in ["save", "salva", "update", "delete", "cria", "create", "alterar"]):
        return "mutation_search"

    # auth
    if any(k in q for k in ["permiss", "role", "auth", "acesso", "permission"]):
        return "auth_search"

    # code location
    if any(k in q for k in ["onde", "arquivo", "função", "classe", "método", "where"]):
        return "code_location_search"

    return None


# ------------------------------
# 2. FALLBACK SEMÂNTICO LEVE
# (sem embeddings ainda: string similarity)
# ------------------------------

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def heuristic_embedding_intent(query: str):
    q = query.lower()

    best_intent = None
    best_score = -1.0

    for intent, seed in INTENT_SEEDS.items():
        if not seed:
            continue

        score = similarity(q, seed)

        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent


# ------------------------------
# 3. INTERFACE FINAL (HYBRID)
# ------------------------------

def detect_intent(query: str):
    # 1. regra primeiro (rápido)
    intent = rule_based_intent(query)
    if intent:
        return intent

    # 2. fallback semântico leve
    return heuristic_embedding_intent(query)
