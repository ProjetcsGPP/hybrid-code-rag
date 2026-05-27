# pipeline_v2/core/relationship/relationship_models.py

from dataclasses import dataclass, field
from typing import Dict
from .relationship_types import RelationshipType


@dataclass
class RelationshipV2:

    id: str

    source: str
    target: str

    type: RelationshipType

    dispatch: str = "DIRECT"

    raw_call: str = ""

    layer: str = "STRUCTURAL"

    status: str = "RESOLVED"

    confidence: float = 1.0

    provenance: str = "AST"

    framework_hint: str = ""

    semantic_owner: str = ""

    metadata: Dict = field(default_factory=dict)
