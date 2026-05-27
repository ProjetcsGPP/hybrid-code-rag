# pipeline_v2/core/runtime/repository_manager.py

from __future__ import annotations


class RepositoryManager:

    def __init__(self, repository):
        self.repository = repository

    def ensure_repository(
        self,
        workspace_id: str,
        project_id: str,
        repository_name: str,
        repository_path: str | None = None,
        metadata: dict | None = None,
    ) -> str:

        repository_id = f"{workspace_id}::{project_id}::{repository_name}"

        self.repository.execute(
            """
            INSERT INTO code_rag.repositories (
                repository_id,
                workspace_id,
                project_id,
                repository_name,
                repository_path,
                metadata,
                created_at
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                NOW()
            )
            ON CONFLICT (repository_id)
            DO NOTHING
            """,
            (
                repository_id,
                workspace_id,
                project_id,
                repository_name,
                repository_path,
                metadata or {},
            ),
        )

        return repository_id
