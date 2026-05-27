# pipeline_v2/core/storage/graph/graph_repository.py

import sqlite3
import json
from .graph_schema import NodeRecordV2, EdgeRecordV2


class GraphRepositoryV2:

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._init_tables()

    # -------------------------
    # SCHEMA
    # -------------------------
    def _init_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY,
            type TEXT,
            name TEXT,
            canonical TEXT,
            metadata TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS edges (
            id TEXT PRIMARY KEY,
            source TEXT,
            target TEXT,
            type TEXT,
            layer TEXT,
            status TEXT,
            confidence REAL,
            metadata TEXT
        )
        """)

        self.conn.commit()

    # -------------------------
    # NODE OPS
    # -------------------------
    def save_node(self, node: NodeRecordV2):
        cursor = self.conn.cursor()

        cursor.execute(
            """
        INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?, ?)
        """,
            (node.id, node.type, node.name, node.canonical, json.dumps(node.metadata)),
        )

        self.conn.commit()

    def get_node(self, node_id: str):
        cursor = self.conn.cursor()

        row = cursor.execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()

        return row

    # -------------------------
    # EDGE OPS
    # -------------------------
    def save_edge(self, edge: EdgeRecordV2):
        cursor = self.conn.cursor()

        cursor.execute(
            """
        INSERT OR REPLACE INTO edges VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                edge.id,
                edge.source,
                edge.target,
                edge.type,
                edge.layer,
                edge.status,
                edge.confidence,
                json.dumps(edge.metadata),
            ),
        )

        self.conn.commit()

    def get_edges_from(self, node_id: str):
        cursor = self.conn.cursor()

        return cursor.execute(
            "SELECT * FROM edges WHERE source = ?", (node_id,)
        ).fetchall()
