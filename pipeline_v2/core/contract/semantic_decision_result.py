# pipeline_v2/core/contract/semantic_decision_result.py

# pipeline_v2/core/contract/semantic_decision_result.py

from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticDecisionResult:
    """
    Decisão final produzida por SemanticAuthority.

    Representa a verdade semântica consolidada
    para um símbolo dentro do pipeline.

    NÃO altera VariableState.

    NÃO representa inferência.

    NÃO representa relacionamento.

    Apenas a decisão final da autoridade semântica.
    """

    variable: str

    semantic_type: str

    model: str | None

    confidence: float

    dispatch: str

    provenance: str

    def to_dict(self) -> dict:
        return {
            "variable": self.variable,
            "semantic_type": self.semantic_type,
            "model": self.model,
            "confidence": self.confidence,
            "dispatch": self.dispatch,
            "provenance": self.provenance,
        }
