# pipeline_v2/core/runtime/snapshot_manager.py

from __future__ import annotations

import hashlib
from datetime import datetime

from pipeline_v2.contracts.runtime.repository_snapshot import (
    RepositorySnapshot,
)


class SnapshotManager:

    def __init__(self, repository):
        self.repository = repository

    def create_snapshot(
        self,
        workspace_id: str,
        project_id: str,
        repository_id: str,
        branch: str | None = None,
        commit_hash: str | None = None,
        metadata: dict | None = None,
    ) -> RepositorySnapshot:

        raw = (
            f"{workspace_id}:"
            f"{project_id}:"
            f"{repository_id}:"
            f"{branch}:"
            f"{commit_hash}:"
            f"{datetime.utcnow().isoformat()}"
        )

        snapshot_id = hashlib.sha256(raw.encode()).hexdigest()

        self.repository.execute(
            """
            INSERT INTO code_rag.repository_snapshots (
                snapshot_id,
                workspace_id,
                project_id,
                repository_id,
                branch,
                commit_hash,
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
                %s,
                NOW()
            )
            """,
            (
                snapshot_id,
                workspace_id,
                project_id,
                repository_id,
                branch,
                commit_hash,
                metadata or {},
            ),
        )

        return RepositorySnapshot(
            snapshot_id=snapshot_id,
            workspace_id=workspace_id,
            project_id=project_id,
            repository_id=repository_id,
            branch=branch,
            commit_hash=commit_hash,
            metadata=metadata or {},
        )
