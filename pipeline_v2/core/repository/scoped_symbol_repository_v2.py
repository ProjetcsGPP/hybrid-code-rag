# pipeline_v2/core/repository/scoped_symbol_repository_v2.py

from pipeline_v2.core.repository.scoped_repository_mixin_v2 import (
    ScopedRepositoryMixinV2,
)


class ScopedSymbolRepositoryV2(
    ScopedRepositoryMixinV2,
):

    def __init__(self, repository):
        self.repository = repository

    # =====================================================
    # INSERT
    # =====================================================

    def upsert_symbol(
        self,
        symbol,
        scope,
    ):

        payload = self._merge_scope(
            {
                "symbol_id": symbol.symbol_id,
                "canonical_name": symbol.canonical_name,
                "name": symbol.name,
                "symbol_type": symbol.symbol_type,
                "file_path": symbol.file_path,
                "module_name": symbol.module_name,
                "symbol_path": symbol.symbol_path,
                "semantic_type": getattr(
                    symbol,
                    "semantic_type",
                    None,
                ),
            },
            scope,
        )

        self.repository.execute(
            """
            INSERT INTO graph_v2.symbols (
                workspace_id,
                project_id,
                repository_id,
                scope_key,

                symbol_id,
                canonical_name,
                name,
                symbol_type,
                file_path,
                module_name,
                symbol_path,
                semantic_type
            )
            VALUES (
                %(workspace_id)s,
                %(project_id)s,
                %(repository_id)s,
                %(scope_key)s,

                %(symbol_id)s,
                %(canonical_name)s,
                %(name)s,
                %(symbol_type)s,
                %(file_path)s,
                %(module_name)s,
                %(symbol_path)s,
                %(semantic_type)s
            )
            ON CONFLICT (
                scope_key,
                canonical_name
            )
            DO UPDATE SET
                semantic_type = EXCLUDED.semantic_type
            """,
            payload,
        )

    # =====================================================
    # LOOKUP
    # =====================================================

    def find_by_canonical_name(
        self,
        canonical_name: str,
        scope,
    ):

        return self.repository.fetch_one(
            """
            SELECT *
            FROM graph_v2.symbols
            WHERE
                scope_key = %(scope_key)s
                AND canonical_name = %(canonical_name)s
            """,
            {
                "scope_key": scope.scope_key,
                "canonical_name": canonical_name,
            },
        )

    def find_by_name(
        self,
        name: str,
        scope,
    ):

        return self.repository.fetch_all(
            """
            SELECT *
            FROM graph_v2.symbols
            WHERE
                scope_key = %(scope_key)s
                AND name = %(name)s
            """,
            {
                "scope_key": scope.scope_key,
                "name": name,
            },
        )
