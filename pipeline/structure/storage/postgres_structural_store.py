# pipeline/structure/storage/postgres_structural_store.py

import json

from pipeline.structure.storage.postgres_connection import (
    PostgresConnection,
)


class PostgresStructuralStore:

    def __init__(
        self,
        connection: PostgresConnection,
        schema: str = "migration_legacy",
    ):

        self.connection = connection
        self.conn = connection.conn
        self.schema = schema

    # =====================================================
    # SYMBOLS
    # =====================================================

    def save_symbol(self, symbol):

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            INSERT INTO {self.schema}.symbols (
                symbol_id,
                symbol_path,
                canonical_name,
                name,
                symbol_type,
                module_name,
                file_path,
                parent_symbol_id,
                semantic_type,
                start_line,
                end_line,
                calls,
                imports
            )
            VALUES (
                %(symbol_id)s,
                %(symbol_path)s,
                %(canonical_name)s,
                %(name)s,
                %(symbol_type)s,
                %(module_name)s,
                %(file_path)s,
                %(parent_symbol_id)s,
                %(semantic_type)s,
                %(start_line)s,
                %(end_line)s,
                %(calls)s,
                %(imports)s
            )
            ON CONFLICT (symbol_id)
            DO UPDATE SET
                canonical_name = EXCLUDED.canonical_name,
                name = EXCLUDED.name,
                symbol_type = EXCLUDED.symbol_type,
                module_name = EXCLUDED.module_name,
                file_path = EXCLUDED.file_path,
                semantic_type = EXCLUDED.semantic_type,
                calls = EXCLUDED.calls,
                imports = EXCLUDED.imports
            """,
            {
                "symbol_id": symbol.symbol_id,
                "symbol_path": symbol.symbol_path,
                "canonical_name": symbol.canonical_name,
                "name": symbol.name,
                "symbol_type": symbol.symbol_type,
                "module_name": symbol.module_name,
                "file_path": symbol.file_path,
                "parent_symbol_id": symbol.parent_symbol_id,
                "semantic_type": symbol.semantic_type,
                "start_line": symbol.start_line,
                "end_line": symbol.end_line,
                "calls": json.dumps(symbol.calls),
                "imports": json.dumps(symbol.imports),
            },
        )

    def get_symbol(self, symbol_id: str):

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM {self.schema}.symbols
            WHERE symbol_id = %s
            """,
            (symbol_id,),
        )

        return cursor.fetchone()

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    def save_relationship(self, relationship):

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            INSERT INTO {self.schema}.relationships (
                relationship_id,
                source_symbol_id,
                target_symbol_id,
                relationship_type,
                metadata
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (relationship_id)
            DO NOTHING
            """,
            (
                relationship.relationship_id,
                relationship.source_symbol_id,
                relationship.target_symbol_id,
                relationship.relationship_type,
                json.dumps(relationship.metadata),
            ),
        )

    def get_relationships(self, symbol_id: str):

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM {self.schema}.relationships
            WHERE source_symbol_id = %s
               OR target_symbol_id = %s
            """,
            (
                symbol_id,
                symbol_id,
            ),
        )

        return cursor.fetchall()

    # =====================================================
    # SEMANTIC REFERENCES
    # =====================================================

    def save_semantic_reference(self, reference):

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            INSERT INTO {self.schema}.semantic_references (
                reference_id,
                source_symbol_id,
                target_symbol_id,
                reference_type,
                confidence,
                metadata
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (reference_id)
            DO NOTHING
            """,
            (
                reference.reference_id,
                reference.source_symbol_id,
                reference.target_symbol_id,
                reference.reference_type,
                reference.confidence,
                json.dumps(reference.metadata),
            ),
        )

    # =====================================================
    # STATS
    # =====================================================

    def get_graph_stats(self):

        cursor = self.conn.cursor()

        cursor.execute(f"SELECT COUNT(*) AS count FROM {self.schema}.symbols")

        nodes = cursor.fetchone()["count"]

        cursor.execute(f"SELECT COUNT(*) AS count FROM {self.schema}.relationships")

        edges = cursor.fetchone()["count"]

        return {
            "nodes": nodes,
            "edges": edges,
        }
