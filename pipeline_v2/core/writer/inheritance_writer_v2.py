# pipeline_v2/core/writer/inheritance_writer_v2.py


class InheritanceWriterV2:

    def __init__(
        self,
        graph_store,
    ):

        self.graph_store = graph_store

    def write(
        self,
        symbol,
        scope,
    ):

        for base in getattr(
            symbol,
            "bases",
            [],
        ):

            self.graph_store.execute(
                """
                INSERT INTO graph_v2.inheritance_edges (
                    workspace_id,
                    project_id,
                    repository_id,
                    scope_key,

                    child_symbol_id,
                    base_symbol_name,
                    resolved_base_symbol_id,
                    confidence,
                    created_at
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,

                    %s,
                    %s,
                    %s,
                    %s,
                    NOW()
                )
                """,
                (
                    scope.workspace_id,
                    scope.project_id,
                    scope.repository_id,
                    scope.scope_key,
                    symbol.symbol_id,
                    base,
                    None,
                    1.0,
                ),
            )
