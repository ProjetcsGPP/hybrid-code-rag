# pipeline_v2/core/namespace/namespace_resolver.py

from pathlib import Path


class NamespaceResolver:
    """
    Resolve contexto lógico
    do repositório.
    """

    def resolve_repository_name(
        self,
        repository_path: str,
    ) -> str:

        return Path(repository_path).name
