# pipeline_v2/contracts/semantic_event.py

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class SemanticEvent:
    """
    Unidade atômica de significado do CODE-RAG.
    """

    event_type: str

    source_symbol: Optional[str]
    target_symbol: Optional[str]

    raw_call: Optional[str]

    confidence: float

    provenance: str  # legacy | v2 | runtime | import | ast

    metadata: Dict
