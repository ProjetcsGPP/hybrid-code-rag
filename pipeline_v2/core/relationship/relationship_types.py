# pipeline_v2/core/relationship/relationship_types.py

from enum import Enum


class RelationshipType(str, Enum):

    # base
    CALLS = "CALLS"

    # semantic dispatch
    SELF_CALL = "SELF_CALL"
    SUPER_CALL = "SUPER_CALL"

    # semantic inference
    ORM_QUERY = "ORM_QUERY"
    ORM_QUERYSET_CALL = "ORM_QUERYSET_CALL"

    INSTANCE_METHOD_CALL = "INSTANCE_METHOD_CALL"
    CHAINED_ATTRIBUTE_CALL = "CHAINED_ATTRIBUTE_CALL"

    # framework
    FRAMEWORK_CALL = "FRAMEWORK_CALL"

    # structure
    IMPORT_RESOLUTION = "IMPORT_RESOLUTION"
    ATTRIBUTE_CALL = "ATTRIBUTE_CALL"
    BELONGS_TO = "BELONGS_TO"
    REFERENCES = "REFERENCES"
    INHERITS = "INHERITS"

    # runtime
    RUNTIME_CALL = "RUNTIME_CALL"

    # unresolved
    UNKNOWN = "UNKNOWN"
