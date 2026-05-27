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
