from pipeline.intent.intent_classifier import detect_intent

tests = [
    "onde esse arquivo faz validação?",
    "onde salva usuário?",
    "onde define permissões?",
    "qual classe define roles?",
    "onde está o método clean?"
]

for q in tests:
    print("\nQ:", q)
    print("INTENT:", detect_intent(q))