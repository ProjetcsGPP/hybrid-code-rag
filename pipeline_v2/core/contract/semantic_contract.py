# pipeline_v2/core/contract/semantic_contract.py

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


# -------------------------
# CHUNK CONTRACT
# -------------------------
@dataclass
class ChunkContract:
    id: str
    file: str
    name: str
    type: str
    raw_calls: List[str] = field(default_factory=list)
    assignments: List[dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# -------------------------
# SYMBOL CONTRACT (ESTÁVEL)
# -------------------------
@dataclass
class SymbolContract:
    id: str
    name: str
    type: str
    file_path: str

    canonical: str

    # 🔥 ESTRUTURA MÍNIMA DO GRAFO (NÃO REMOVER)
    parent: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# -------------------------
# RELATIONSHIP CONTRACT
# -------------------------
@dataclass
class RelationshipContract:
    id: str
    source: str
    target: str
    type: str

    layer: str = "SEMANTIC"
    status: str = "RESOLVED"

    dispatch: str = "DIRECT"

    raw_call: str = ""

    confidence: float = 1.0

    provenance: str = "AST_DIRECT"

    framework_hint: str = ""

    semantic_owner: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)
