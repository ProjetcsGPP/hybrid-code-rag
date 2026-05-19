# pipeline_v2/core/relationship/relationship_resolver.py

from .relationship_types import RelationshipType


class RelationshipResolverV2:

    def resolve_call(self, caller_symbol, raw_call: str):

        if raw_call.startswith("self."):
            return RelationshipType.SELF_CALL, "SELF"

        if raw_call.startswith("super."):
            return RelationshipType.SUPER_CALL, "SUPER"

        if "objects." in raw_call:
            return RelationshipType.ORM_QUERY, "ORM"

        if "." in raw_call:
            return RelationshipType.FRAMEWORK_CALL, "FRAMEWORK"

        return RelationshipType.CALLS, "DIRECT"
