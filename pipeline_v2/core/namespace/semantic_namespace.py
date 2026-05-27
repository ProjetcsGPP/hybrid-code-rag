# pipeline_v2/core/namespace/semantic_namespace.py

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class SemanticNamespace:

    namespace_id: str

    workspace_id: str

    project_id: str

    repository_id: str

    branch: str = "main"

    language: str | None = None

    framework: str | None = None

    partition_key: str | None = None

    metadata: Dict[str, Any] = field(default_factory=dict)
