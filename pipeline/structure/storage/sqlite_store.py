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
        db_path: str = (
            "storage/structural/structure.db"
        ),
    ):

        self.db_path = db_path

        self._ensure_directory()

        self.conn = sqlite3.connect(
            self.db_path
        )

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

        db_dir = Path(
            self.db_path
        ).parent

        db_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _initialize_schema(self):

        cursor = self.conn.cursor()

        # =============================================
        # SYMBOLS
        # =============================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS symbols (

                symbol_id TEXT PRIMARY KEY,

                symbol_path TEXT,
                name TEXT,

                symbol_type TEXT,

                module_name TEXT,
                file_path TEXT,

                parent_symbol_id TEXT,

                semantic_type TEXT,

                start_line INTEGER,
                end_line INTEGER
            )
            """
        )

        # =============================================
        # RELATIONSHIPS
        # =============================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS relationships (

                relationship_id TEXT PRIMARY KEY,

                source_symbol_id TEXT,
                target_symbol_id TEXT,

                relationship_type TEXT,

                confidence REAL
            )
            """
        )

        # =============================================
        # INDEXES
        # =============================================

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_symbols_name
            ON symbols(name)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_symbols_path
            ON symbols(symbol_path)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_symbols_parent
            ON symbols(parent_symbol_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_relationships_source
            ON relationships(source_symbol_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_relationships_target
            ON relationships(target_symbol_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_relationships_type
            ON relationships(relationship_type)
            """
        )

        self.conn.commit()

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
                name,

                symbol_type,

                module_name,
                file_path,

                parent_symbol_id,

                semantic_type,

                start_line,
                end_line

            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol.symbol_id,

                symbol.symbol_path,
                symbol.name,

                symbol.symbol_type,

                symbol.module_name,
                symbol.file_path,

                symbol.parent_symbol_id,

                symbol.semantic_type,

                symbol.start_line,
                symbol.end_line,
            )
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
            (symbol_id,)
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

                confidence

            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                relationship.relationship_id,

                relationship.source_symbol_id,
                relationship.target_symbol_id,

                relationship.relationship_type,

                relationship.confidence,
            )
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
            )
        )

        return cursor.fetchall()

    # -------------------------------------------------
    # LIFECYCLE
    # -------------------------------------------------

    def close(self):

        if self.conn:
            self.conn.close()