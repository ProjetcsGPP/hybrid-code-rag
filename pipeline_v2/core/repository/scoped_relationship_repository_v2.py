# pipeline_v2/core/repository/scoped_relationship_repository_v2.py

from pipeline_v2.core.repository.scoped_repository_mixin_v2 import (
    ScopedRepositoryMixinV2,
)


class ScopedRelationshipRepositoryV2(
    ScopedRepositoryMixinV2,
):

    def __init__(self, repository):
        self.repository = repository

    def write_relationship(
        self,
        relationship,
        scope,
    ):

        payload = self._merge_scope(
            {
                "relationship_id": relationship.relationship_id,
                "source_symbol_id": relationship.source_symbol_id,
                "target_symbol_id": relationship.target_symbol_id,
                "relationship_type": relationship.relationship_type,
                "confidence": relationship.confidence,
                "metadata": getattr(
                    relationship,
                    "metadata",
                    {},
                ),
            },
            scope,
        )

        self.repository.execute(
            """
            INSERT INTO graph_v2.relationships (
                workspace_id,
                project_id,
                repository_id,
                scope_key,

                relationship_id,
                source_symbol_id,
                target_symbol_id,
                relationship_type,
                confidence,
                metadata
            )
            VALUES (
                %(workspace_id)s,
                %(project_id)s,
                %(repository_id)s,
                %(scope_key)s,

                %(relationship_id)s,
                %(source_symbol_id)s,
                %(target_symbol_id)s,
                %(relationship_type)s,
                %(confidence)s,
                %(metadata)s
            )
            """,
            payload,
        )
