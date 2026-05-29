# pipeline_v2/core/relationship/relationship_factory.py

from .relationship_models import RelationshipV2
from .relationship_types import RelationshipType


class RelationshipFactoryV2:
    """
    Relationship identity is now fully deterministic
    and fully structural.

    No UUID.
    No hashes.
    No external identity generators.
    """

    @staticmethod
    def create(
        source: str,
        target: str,
        type: RelationshipType,
        dispatch: str = "DIRECT",
        raw_call: str = "",
        layer: str = "STRUCTURAL",
        status: str = "RESOLVED",
        confidence: float = 1.0,
        provenance: str = "AST",
        framework_hint: str = "",
        semantic_owner: str = "",
        metadata=None,
    ):

        # =====================================================
        # DETERMINISTIC STRUCTURAL IDENTITY
        # =====================================================

        relationship_type = type.value if hasattr(type, "value") else str(type)

        rel_id = f"{source}::{relationship_type}::{target}"

        # =====================================================
        # BUILD RELATIONSHIP
        # =====================================================

        return RelationshipV2(
            id=rel_id,
            source=source,
            target=target,
            type=type,
            dispatch=dispatch,
            raw_call=raw_call,
            layer=layer,
            status=status,
            confidence=confidence,
            provenance=provenance,
            framework_hint=framework_hint,
            semantic_owner=semantic_owner,
            metadata=metadata or {},
        )
