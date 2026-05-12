# pipeline/structure/resolver/semantic_call.py

from dataclasses import dataclass
from typing import Literal, Optional
from pipeline.contracts import Symbol


CallType = Literal[
    "METHOD",
    "SELF_METHOD",
    "SUPER_METHOD",
    "ORM_MANAGER",
    "FUNCTION",
    "EXTERNAL"
]


@dataclass
class SemanticCallTarget:
    raw: str

    owner_name: Optional[str]
    method: str

    call_type: CallType

    resolved_symbol: Optional[Symbol] = None

    confidence: float = 0.0