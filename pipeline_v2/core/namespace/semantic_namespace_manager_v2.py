# pipeline_v2/core/namespace/semantic_namespace_manager_v2.py

from pipeline_v2.core.profiling.semantic_profile import (
    SemanticProfile,
)

from .semantic_namespace import (
    SemanticNamespace,
)

from .namespace_identity import (
    NamespaceIdentityBuilder,
)

from .namespace_partition import (
    NamespacePartitionBuilder,
)

from .namespace_registry import (
    NamespaceRegistry,
)


class SemanticNamespaceManagerV2:
    """
    Responsável por:

    - criar namespaces
    - isolar contextos
    - gerar identities
    - criar partition keys
    - controlar escopo semântico
    """

    def __init__(self):

        self.identity_builder = NamespaceIdentityBuilder()

        self.partition_builder = NamespacePartitionBuilder()

        self.registry = NamespaceRegistry()

    def create_namespace(
        self,
        workspace_id: str,
        project_id: str,
        repository_id: str,
        semantic_profile: SemanticProfile,
        branch: str = "main",
    ) -> SemanticNamespace:

        namespace_id = self.identity_builder.build(
            workspace_id=workspace_id,
            project_id=project_id,
            repository_id=repository_id,
            branch=branch,
            language=semantic_profile.primary_language,
            framework=semantic_profile.primary_framework,
        )

        partition_key = self.partition_builder.build_partition_key(namespace_id)

        namespace = SemanticNamespace(
            namespace_id=namespace_id,
            workspace_id=workspace_id,
            project_id=project_id,
            repository_id=repository_id,
            branch=branch,
            language=semantic_profile.primary_language,
            framework=semantic_profile.primary_framework,
            partition_key=partition_key,
        )

        self.registry.register(namespace)

        return namespace
