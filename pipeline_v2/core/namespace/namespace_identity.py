# pipeline_v2/core/namespace/namespace_identity.py

import hashlib


class NamespaceIdentityBuilder:
    """
    Gera identidade determinística
    para namespace semântico.
    """

    def build(
        self,
        workspace_id: str,
        project_id: str,
        repository_id: str,
        branch: str,
        language: str | None,
        framework: str | None,
    ) -> str:

        raw = "::".join(
            [
                workspace_id,
                project_id,
                repository_id,
                branch,
                language or "unknown",
                framework or "unknown",
            ]
        )

        return hashlib.sha256(raw.encode()).hexdigest()
