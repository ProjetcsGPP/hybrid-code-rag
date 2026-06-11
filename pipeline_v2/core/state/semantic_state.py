# pipeline_v2/core/state/semantic_state.py

from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class VariableState:
    name: str
    source: str
    semantic_type: Optional[str] = None
    inferred_symbol: Optional[str] = None
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class SemanticState:
    """
    MÍNIMO STATE LAYER

    Responsável por:
    - armazenar assignments
    - rastrear variáveis locais
    - fornecer lookup semântico básico

    NÃO faz propagation completa ainda.
    """

    def __init__(self):
        self.variables: Dict[str, VariableState] = {}

    # -------------------------
    # REGISTER ASSIGNMENT
    # -------------------------
    def set_variable(
        self,
        name: str,
        source: str,
        semantic_type: str = None,
        inferred_symbol: str = None,
        confidence: float = 0.0,
        metadata: dict = None,
    ):
        self.variables[name] = VariableState(
            name=name,
            source=source,
            semantic_type=semantic_type,
            inferred_symbol=inferred_symbol,
            confidence=confidence,
            metadata=metadata or {},
        )

    # -------------------------
    # GET VARIABLE STATE
    # -------------------------
    def resolve_variable(self, name: str) -> Optional[VariableState]:
        return self.variables[name] if name in self.variables else None

    # -------------------------
    # DEBUG HELPERS
    # -------------------------
    def dump(self):
        return {
            k: {
                "source": v.source,
                "semantic_type": v.semantic_type,
                "inferred_symbol": v.inferred_symbol,
                "confidence": v.confidence,
            }
            for k, v in self.variables.items()
        }
