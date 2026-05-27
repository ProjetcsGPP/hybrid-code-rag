# pipeline_v2/core/semantic/symbol/semantic_symbol.py

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class SemanticSymbol:
    """
    Semantic representation layer.

    Objetivo:
    - desacoplar semantic resolution do grafo estrutural
    - permitir múltiplas formas de lookup
    - preparar semantic ownership graph
    """

    canonical: str
    symbol_id: str

    aliases: List[str] = field(default_factory=list)

    imports: List[str] = field(default_factory=list)

    semantic_type: str = "general"

    framework: Optional[str] = None

    inheritance_chain: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)
