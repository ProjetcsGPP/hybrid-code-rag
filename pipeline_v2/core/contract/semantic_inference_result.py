# pipeline_v2/core/contract/semantic_inference_result.py

from dataclasses import dataclass
from typing import Optional

from pipeline_v2.core.relationship.relationship_types import (
    RelationshipType,
)


@dataclass
class SemanticInferenceResult:

    relationship_type: RelationshipType

    dispatch: str

    confidence: float

    semantic_owner: str

    framework_hint: str

    provenance: str

    resolved_call: str

    inferred_symbol: Optional[str] = None
