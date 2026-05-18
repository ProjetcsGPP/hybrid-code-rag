# pipeline/structure/storage/sqlite_store.py

import sqlite3
from pathlib import Path
import os

from pipeline.contracts import (
    Symbol,
    Relationship,
)


class SQLiteStructuralStore:

    def __init__(
        self,
        db_path: str = ("storage/structural/structure.db"),
    ):

        self.db_path = db_path

        self._ensure_directory()

        self.conn = sqlite3.connect(self.db_path)

        self.conn.row_factory = sqlite3.Row

        self._initialize_schema()

    # -------------------------------------------------
    # BOOTSTRAP
    # -------------------------------------------------

    def reset(self):

        if self.conn:
            self.conn.close()

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        self.conn = sqlite3.connect(self.db_path)

        self.conn.row_factory = sqlite3.Row

        self._initialize_schema()

    def _ensure_directory(self):

        db_dir = Path(self.db_path).parent

        db_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _initialize_schema(self):

        cursor = self.conn.cursor()

        # =============================================
        # SYMBOLS
        # =============================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symbols (

                symbol_id TEXT PRIMARY KEY,

                symbol_path TEXT,
                canonical_name TEXT,
                name TEXT,

                symbol_type TEXT,

                module_name TEXT,
                file_path TEXT,

                parent_symbol_id TEXT,

                semantic_type TEXT,

                start_line INTEGER,
                end_line INTEGER
            )
            """)

        # =============================================
        # RELATIONSHIPS
        # =============================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (

                relationship_id TEXT PRIMARY KEY,

                source_symbol_id TEXT,
                target_symbol_id TEXT,

                relationship_type TEXT,

                confidence REAL
            )
            """)

        # =============================================
        # SEMANTIC REFERENCES
        # =============================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semantic_references (

                reference_id TEXT PRIMARY KEY,

                source_symbol_id TEXT,

                reference_type TEXT,

                raw_call TEXT,

                owner TEXT,
                method TEXT,

                confidence REAL
            )
            """)

        # =============================================
        # MIGRATIONS
        # =============================================

        self._ensure_relationship_columns()

        # =============================================
        # INDEXES
        # =============================================

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_symbols_name
            ON symbols(name)
            """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_symbols_path
            ON symbols(symbol_path)
            """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_symbols_parent
            ON symbols(parent_symbol_id)
            """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_relationships_source
            ON relationships(source_symbol_id)
            """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_relationships_target
            ON relationships(target_symbol_id)
            """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_relationships_type
            ON relationships(relationship_type)
            """)

        self.conn.commit()

    # -------------------------------------------------
    # SCHEMA MIGRATION
    # -------------------------------------------------

    def _ensure_relationship_columns(self):

        cursor = self.conn.cursor()

        existing_columns = self._get_table_columns("relationships")

        required_columns = {
            "layer": "TEXT",
            "resolution_status": "TEXT",
            "provenance": "TEXT",
            "dispatch_type": "TEXT",
            "framework_hint": "TEXT",
            "resolver_stage": "TEXT",
        }

        for column_name, column_type in required_columns.items():

            if column_name in existing_columns:
                continue

            print(f"[SCHEMA MIGRATION] " f"Adding relationships.{column_name}")

            cursor.execute(f"""
                ALTER TABLE relationships
                ADD COLUMN {column_name} {column_type}
                """)

        self.conn.commit()

    def _get_table_columns(
        self,
        table_name: str,
    ):

        cursor = self.conn.execute(f"PRAGMA table_info({table_name})")

        rows = cursor.fetchall()

        return {row["name"] for row in rows}

    # -------------------------------------------------
    # SYMBOLS
    # -------------------------------------------------

    def save_symbol(
        self,
        symbol: Symbol,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO symbols (

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
                end_line

            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol.symbol_id,
                symbol.symbol_path,
                symbol.canonical_name,
                symbol.name,
                symbol.symbol_type,
                symbol.module_name,
                symbol.file_path,
                symbol.parent_symbol_id,
                symbol.semantic_type,
                symbol.start_line,
                symbol.end_line,
            ),
        )

        self.conn.commit()

    def get_symbol(
        self,
        symbol_id: str,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM symbols
            WHERE symbol_id = ?
            """,
            (symbol_id,),
        )

        return cursor.fetchone()

    # -------------------------------------------------
    # RELATIONSHIPS
    # -------------------------------------------------

    def save_relationship(
        self,
        relationship: Relationship,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO relationships (

                relationship_id,

                source_symbol_id,
                target_symbol_id,

                relationship_type,

                confidence,

                layer,
                resolution_status,
                provenance,
                dispatch_type,
                framework_hint,
                resolver_stage

            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                relationship.relationship_id,
                relationship.source_symbol_id,
                relationship.target_symbol_id,
                relationship.relationship_type,
                relationship.confidence,
                relationship.layer,
                relationship.resolution_status,
                relationship.provenance,
                relationship.dispatch_type,
                relationship.framework_hint,
                relationship.resolver_stage,
            ),
        )

        self.conn.commit()

    def get_relationships(
        self,
        symbol_id: str,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM relationships
            WHERE source_symbol_id = ?
               OR target_symbol_id = ?
            """,
            (
                symbol_id,
                symbol_id,
            ),
        )

        return cursor.fetchall()

    # -------------------------------------------------
    # LIFECYCLE
    # -------------------------------------------------

    def close(self):

        if self.conn:
            self.conn.close()

    # -------------------------------------------------
    # GRAPH STATS
    # -------------------------------------------------

    def get_graph_stats(self):

        cursor = self.conn.cursor()

        nodes = cursor.execute("""
            SELECT COUNT(*)
            FROM symbols
            """).fetchone()[0]

        edges = cursor.execute("""
            SELECT COUNT(*)
            FROM relationships
            """).fetchone()[0]

        references = cursor.execute("""
            SELECT COUNT(*)
            FROM semantic_references
            """).fetchone()[0]

        return {
            "nodes": nodes,
            "edges": edges,
            "references": references,
        }

    # -------------------------------------------------
    # SEMANTIC REFERENCES
    # -------------------------------------------------

    def get_all_semantic_references(self):

        cursor = self.conn.execute("""
            SELECT
                reference_id,
                source_symbol_id,
                reference_type,
                raw_call,
                owner,
                method,
                confidence
            FROM semantic_references
            """)

        return cursor.fetchall()

    def save_semantic_reference(
        self,
        reference,
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO semantic_references (

                reference_id,

                source_symbol_id,

                reference_type,

                raw_call,

                owner,
                method,

                confidence

            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                reference.reference_id,
                reference.source_symbol_id,
                reference.reference_type,
                reference.raw_call,
                reference.owner,
                reference.method,
                reference.confidence,
            ),
        )

        self.conn.commit()
