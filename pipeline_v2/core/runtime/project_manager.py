# pipeline_v2/core/runtime/project_manager.py

from __future__ import annotations


class ProjectManager:

    def __init__(self, repository):
        self.repository = repository

    def ensure_project(
        self,
        workspace_id: str,
        project_name: str,
        metadata: dict | None = None,
    ) -> str:

        project_id = f"{workspace_id}::{project_name}"

        self.repository.execute(
            """
            INSERT INTO code_rag.projects (
                project_id,
                workspace_id,
                project_name,
                metadata,
                created_at
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                NOW()
            )
            ON CONFLICT (project_id)
            DO NOTHING
            """,
            (
                project_id,
                workspace_id,
                project_name,
                metadata or {},
            ),
        )

        return project_id
