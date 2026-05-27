# pipeline_v2/contracts/runtime/semantic_runtime_context.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SemanticRuntimeContext:

    workspace_id: str
    project_id: str
    repository_id: str

    branch: Optional[str] = None
    commit_hash: Optional[str] = None

    language_profile_id: Optional[str] = None
    framework_profile_id: Optional[str] = None

    snapshot_id: Optional[str] = None

    metadata: dict = field(default_factory=dict)

    @property
    def namespace(self) -> str:

        parts = [
            self.workspace_id,
            self.project_id,
            self.repository_id,
        ]

        if self.branch:
            parts.append(self.branch)

        return ".".join(parts)
