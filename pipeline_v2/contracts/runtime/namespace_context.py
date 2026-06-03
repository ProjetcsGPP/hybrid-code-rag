# pipeline_v2/contracts/runtime/namespace_context.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NamespaceContext:

    workspace_id: str
    project_id: str
    repository_id: str

    module_name: Optional[str] = None
    file_path: Optional[str] = None

    branch: Optional[str] = None
    commit_hash: Optional[str] = None

    metadata: dict = field(default_factory=dict)

    @property
    def namespace(self) -> str:

        self.validate()

        parts = [
            self.workspace_id,
            self.project_id,
            self.repository_id,
        ]

        if self.module_name:
            parts.append(self.module_name)

        return ".".join(parts)

    def build_symbol_namespace(
        self,
        symbol_name: str,
    ) -> str:

        if not symbol_name:
            raise ValueError("symbol_name required")

        return f"{self.namespace}.{symbol_name}"

    def validate(self):

        if not self.workspace_id:
            raise ValueError("workspace_id required")

        if not self.project_id:
            raise ValueError("project_id required")

        if not self.repository_id:
            raise ValueError("repository_id required")

        return self
