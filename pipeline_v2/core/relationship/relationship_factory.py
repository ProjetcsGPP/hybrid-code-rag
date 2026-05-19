# pipeline_v2/core/relationship/relationship_factory.py

import uuid
from .relationship_models import RelationshipV2
from .relationship_types import RelationshipType


class RelationshipFactoryV2:

    @staticmethod
    def create(
        source: str,
        target: str,
        type: RelationshipType,
        layer: str = "STRUCTURAL",
        status: str = "RESOLVED",
        confidence: float = 1.0,
        metadata=None,
    ):

        rel_id = f"{type.value}::{source}::{target}::{uuid.uuid4().hex[:6]}"

        return RelationshipV2(
            id=rel_id,
            source=source,
            target=target,
            type=type,
            layer=layer,
            status=status,
            confidence=confidence,
            metadata=metadata or {},
        )
