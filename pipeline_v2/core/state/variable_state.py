# pipeline_v2/core/state/variable_state.py

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
