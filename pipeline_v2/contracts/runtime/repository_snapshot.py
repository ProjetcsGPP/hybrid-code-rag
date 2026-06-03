# pipeline_v2/contracts/runtime/repository_snapshot.py


from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class RepositorySnapshot:

    snapshot_id: str

    workspace_id: str
    project_id: str
    repository_id: str

    branch: Optional[str] = None
    commit_hash: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.utcnow)

    metadata: dict = field(default_factory=dict)

    def __post_init__(self):

        self.validate()

    def validate(self):

        if not self.workspace_id:
            raise ValueError("workspace_id required")

        if not self.project_id:
            raise ValueError("project_id required")

        if not self.repository_id:
            raise ValueError("repository_id required")

        return self
