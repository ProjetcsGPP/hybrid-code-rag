# pipeline_v2/core/context/semantic_scope_factory_v2.py

from pathlib import Path

from pipeline_v2.core.context.semantic_scope_v2 import (
    SemanticScopeV2,
)


class SemanticScopeFactoryV2:

    def create_from_repository(
        self,
        repository_path: str,
        language_profile=None,
        framework_profiles=None,
    ) -> SemanticScopeV2:

        path = Path(repository_path)

        repository_id = path.name
        project_id = path.parent.name
        workspace_id = path.parent.parent.name

        return SemanticScopeV2(
            workspace_id=workspace_id,
            project_id=project_id,
            repository_id=repository_id,
            language_profile=language_profile,
            framework_profiles=framework_profiles or [],
        )
