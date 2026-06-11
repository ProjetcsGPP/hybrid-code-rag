from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class VariableState:
    """
    Estado semântico transitório de variável.

    NÃO representa persistência global.
    Apenas contexto semântico local do chunk.
    """

    name: str

    # origem da inferência
    source: Optional[str] = None

    # semantic info
    semantic_type: str = "unknown"

    # ORM/model awareness
    model: Optional[str] = None

    # symbol inference
    inferred_symbol: Optional[str] = None

    # semantic quality
    confidence: float = 0.0

    # provenance / framework
    framework_hint: Optional[str] = None
    provenance: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    # =========================================================
    # NORMALIZAÇÃO INTERNA (EVITA ESTADO CORROMPIDO)
    # =========================================================
    def __post_init__(self):
        self.semantic_type = self._normalize_semantic_type(self.semantic_type)
        self.confidence = self._normalize_confidence(self.confidence)

    def _normalize_semantic_type(self, value: str) -> str:
        valid = {
            "instance",
            "queryset",
            "attribute_chain",
            "unknown",
        }
        return value if value in valid else "unknown"

    def _normalize_confidence(self, value: float) -> float:
        try:
            value = float(value)
        except Exception:
            return 0.0

        return max(0.0, min(1.0, round(value, 4)))

    # =========================================================
    # SERIALIZAÇÃO SEGURA (SUBSTITUI vars(v))
    # =========================================================
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "source": self.source,
            "semantic_type": self.semantic_type,
            "model": self.model,
            "inferred_symbol": self.inferred_symbol,
            "confidence": self.confidence,
            "framework_hint": self.framework_hint,
            "provenance": self.provenance,
            "metadata": self.metadata,
        }

    # =========================================================
    # DEBUG SAFE (evita vazamento de referência interna)
    # =========================================================
    def dump(self) -> Dict[str, Any]:
        return self.to_dict()
