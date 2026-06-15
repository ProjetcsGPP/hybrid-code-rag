# pipeline_v2/core/contract/relationship_resolution_result.py


from dataclasses import dataclass, field

from pipeline_v2.core.relationship.relationship_types import (
    RelationshipType,
)

from pipeline_v2.core.context.semantic_resolution_payload import (
    SemanticResolutionPayload,
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

    semantic: SemanticResolutionPayload = field(
        default_factory=SemanticResolutionPayload
    )

    def to_dict(self) -> dict:
        return {
            "relationship_type": (
                self.relationship_type.value
                if hasattr(self.relationship_type, "value")
                else self.relationship_type
            ),
            "dispatch": self.dispatch,
            "semantic": (self.semantic.to_dict() if self.semantic else None),
            "layer": self.layer,
            "normalized_call": self.normalized_call,
            "confidence": self.confidence,
            "resolution_path": self.resolution_path,
        }
