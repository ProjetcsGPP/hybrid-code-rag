# pipeline_v2/core/namespace/namespace_types.py

from enum import Enum


class NamespaceIsolationLevel(str, Enum):

    WORKSPACE = "workspace"

    PROJECT = "project"

    REPOSITORY = "repository"

    BRANCH = "branch"


class NamespacePartitionType(str, Enum):

    GRAPH = "graph"

    VECTOR = "vector"

    CACHE = "cache"
