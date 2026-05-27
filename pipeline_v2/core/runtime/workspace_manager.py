# pipeline_v2/core/runtime/workspace_manager.py

from __future__ import annotations


class WorkspaceManager:

    def __init__(self, repository):
        self.repository = repository

    def ensure_workspace(
        self,
        workspace_name: str,
        metadata: dict | None = None,
    ) -> str:

        workspace_id = workspace_name.lower().replace(" ", "_")

        self.repository.execute(
            """
            INSERT INTO code_rag.workspaces (
                workspace_id,
                workspace_name,
                metadata,
                created_at
            )
            VALUES (
                %s,
                %s,
                %s,
                NOW()
            )
            ON CONFLICT (workspace_id)
            DO NOTHING
            """,
            (
                workspace_id,
                workspace_name,
                metadata or {},
            ),
        )

        return workspace_id
