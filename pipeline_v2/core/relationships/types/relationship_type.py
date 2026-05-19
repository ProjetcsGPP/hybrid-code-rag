# pipeline_v2/core/relationships/types/relationship_type.py

from enum import Enum


class RelationshipType(str, Enum):
    CALLS = "calls"
    BELONGS_TO = "belongs_to"
    IMPORTS = "imports"
    REFERENCES = "references"
    INHERITS = "inherits"

    # EXTENSÕES FUTURAS (Next.js / React)
    FRAMEWORK_HOOK = "framework_hook"  # useEffect, useState
    ROUTE_BINDING = "route_binding"  # Next.js routing
    SERVER_ACTION = "server_action"  # Next.js actions
    COMPONENT_USE = "component_use"  # React component usage
