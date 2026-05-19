#

from dataclasses import dataclass, field
from typing import Dict
from .relationship_types import RelationshipType


@dataclass
class RelationshipV2:
    id: str

    source: str
    target: str

    type: RelationshipType

    layer: str  # STRUCTURAL | SEMANTIC | RUNTIME
    status: str  # RESOLVED | UNRESOLVED | APPROXIMATE

    confidence: float = 1.0

    metadata: Dict = field(default_factory=dict)
