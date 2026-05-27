# pipeline_v2/core/relationship/relationship_factory.py

from .relationship_models import RelationshipV2
from .relationship_types import RelationshipType

from pipeline_v2.core.identity.deterministic_identity import DeterministicIdentity
from pipeline_v2.core.identity.identity_strategy import IdentityStrategy


class RelationshipFactoryV2:

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
        strategy: IdentityStrategy = IdentityStrategy(),
    ):
        """
        Factory semântica determinística.
        """

        # -------------------------------------------------
        # 1. BUILD CONTEXT VIA STRATEGY
        # -------------------------------------------------

        context = strategy.build_relationship_context(
            source=source,
            target=target,
            relationship_type=type.value if hasattr(type, "value") else str(type),
            dispatch=dispatch,
            layer=layer,
            raw_call=raw_call,
        )

        # -------------------------------------------------
        # 2. DETERMINISTIC RELATIONSHIP ID
        # -------------------------------------------------

        rel_id = DeterministicIdentity.relationship_id(
            source=context["source"],
            target=context["target"],
            relationship_type=context["relationship_type"],
            dispatch=context["dispatch"],
            layer=context["layer"],
            namespace=context["namespace"],
            raw_call=context["raw_call"],
        )

        # -------------------------------------------------
        # 3. BUILD RELATIONSHIP OBJECT
        # -------------------------------------------------

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
