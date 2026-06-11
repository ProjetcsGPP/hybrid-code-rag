# pipeline_v2/core/contract/semantic_inference_result.py

from dataclasses import dataclass
from typing import Optional

from pipeline_v2.core.relationship.relationship_types import (
    RelationshipType,
)


@dataclass(frozen=True)
class SemanticInferenceResult:

    relationship_type: RelationshipType

    dispatch: str

    confidence: float

    semantic_owner: str

    framework_hint: str

    provenance: str

    resolved_call: str

    inferred_symbol: Optional[str] = None

    def to_dict(self):

        return {
            "relationship_type": (
                self.relationship_type.value
                if hasattr(self.relationship_type, "value")
                else self.relationship_type
            ),
            "dispatch": self.dispatch,
            "confidence": self.confidence,
            "semantic_owner": self.semantic_owner,
            "framework_hint": self.framework_hint,
            "provenance": self.provenance,
            "resolved_call": self.resolved_call,
            "inferred_symbol": self.inferred_symbol,
        }
