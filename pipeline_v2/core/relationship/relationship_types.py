# pipeline_v2/core/relationship/relationship_types.py

from enum import Enum


class RelationshipType(str, Enum):
    CALLS = "CALLS"
    SUPER_CALL = "SUPER_CALL"
    SELF_CALL = "SELF_CALL"
    ORM_QUERY = "ORM_QUERY"
    FRAMEWORK_CALL = "FRAMEWORK_CALL"
    IMPORT_RESOLUTION = "IMPORT_RESOLUTION"
    ATTRIBUTE_CALL = "ATTRIBUTE_CALL"
    UNKNOWN = "UNKNOWN"
