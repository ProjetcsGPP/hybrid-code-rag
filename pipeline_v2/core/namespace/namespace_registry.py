# pipeline_v2/core/namespace/namespace_registry.py

from .semantic_namespace import SemanticNamespace


class NamespaceRegistry:

    def __init__(self):

        self._namespaces = {}

    def register(
        self,
        namespace: SemanticNamespace,
    ):

        self._namespaces[namespace.namespace_id] = namespace

    def get(
        self,
        namespace_id: str,
    ) -> SemanticNamespace | None:

        return (
            self._namespaces[namespace_id]
            if namespace_id in self._namespaces
            else None
        )
