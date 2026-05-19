# pipeline_v2/core/relationships/relationship.py

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from .types.relationship_type import RelationshipType


@dataclass
class Relationship:
    """
    Relationship V2 - aresta do grafo semântico universal.

    Conecta símbolos independentemente de linguagem.
    """

    id: str

    source_id: str
    target_id: str

    relationship_type: RelationshipType

    # confiança do resolver (0.0 - 1.0)
    confidence: float = 1.0

    # camada semântica (STRUCTURAL / SEMANTIC / RUNTIME)
    layer: str = "STRUCTURAL"

    # como foi resolvido
    resolution_method: str = "AST"

    # framework hint (django, nextjs, react...)
    framework: Optional[str] = None

    # metadados extensíveis
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_high_confidence(self) -> bool:
        return self.confidence >= 0.8

    def is_runtime_approximation(self) -> bool:
        return self.layer == "RUNTIME"
