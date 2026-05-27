# pipeline_v2/core/context/semantic_scope_v2.py

from dataclasses import dataclass, field
from typing import Optional
from typing import List


@dataclass(slots=True)
class SemanticScopeV2:

    # ==========================================
    # WORKSPACE
    # ==========================================

    workspace_id: str

    # ==========================================
    # PROJECT
    # ==========================================

    project_id: str

    repository_id: str

    # ==========================================
    # SOURCE CONTROL
    # ==========================================

    branch: Optional[str] = None

    commit_hash: Optional[str] = None

    # ==========================================
    # LANGUAGE CONTEXT
    # ==========================================

    language_profile: Optional[str] = None

    language_family: Optional[str] = None

    framework_profiles: List[str] = field(default_factory=list)

    # ==========================================
    # RUNTIME CONTEXT
    # ==========================================

    runtime_environment: Optional[str] = None

    execution_context: Optional[str] = None

    # ==========================================
    # METADATA
    # ==========================================

    metadata: dict = field(default_factory=dict)

    # ==========================================
    # HELPERS
    # ==========================================

    @property
    def scope_key(self) -> str:

        return f"{self.workspace_id}::" f"{self.project_id}::" f"{self.repository_id}"

    def build_scoped_symbol_id(
        self,
        canonical_name: str,
    ) -> str:

        return f"{self.scope_key}::{canonical_name}"
