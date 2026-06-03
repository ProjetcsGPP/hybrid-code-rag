# pipeline_v2/core/contract/relationship_resolution_result.py


from dataclasses import dataclass, field
from typing import Dict, Any

from pipeline_v2.core.relationship.relationship_types import (
    RelationshipType,
)


@dataclass
class RelationshipResolutionResult:
    """
    Resultado produzido por RelationshipResolverV2.

    Não representa uma aresta.
    Não representa persistência.

    Representa apenas o resultado da etapa de resolução.
    """

    relationship_type: RelationshipType

    dispatch: str

    layer: str

    normalized_call: str

    confidence: float

    resolution_path: str

    semantic: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "relationship_type": self.relationship_type,
            "dispatch": self.dispatch,
            "semantic": self.semantic,
            "layer": self.layer,
            "normalized_call": self.normalized_call,
            "confidence": self.confidence,
            "resolution_path": self.resolution_path,
        }
