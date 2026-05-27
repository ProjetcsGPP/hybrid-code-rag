# pipeline_v2/core/repository/scoped_repository_mixin_v2.py


class ScopedRepositoryMixinV2:

    def _scope_filter(
        self,
        scope,
    ):

        return {
            "workspace_id": scope.workspace_id,
            "project_id": scope.project_id,
            "repository_id": scope.repository_id,
            "scope_key": scope.scope_key,
        }

    def _merge_scope(
        self,
        payload: dict,
        scope,
    ):

        return {
            **payload,
            **self._scope_filter(scope),
        }
