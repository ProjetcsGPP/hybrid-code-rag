# pipeline_v2/core/storage/graph/graph_repository_postgres.py

import json

from pipeline_v2.core.storage.graph.graph_schema import (
    NodeRecordV2,
    EdgeRecordV2,
)


class GraphRepositoryPostgresV2:

    def __init__(
        self,
        connection,
        schema: str = "migration_v2",
    ):

        self.connection = connection
        self.conn = connection.conn
        self.schema = schema

    # =====================================================
    # NODE OPS
    # =====================================================

    def save_node(self, node: NodeRecordV2):

        if not isinstance(node, NodeRecordV2):
            raise TypeError(f"Expected NodeRecordV2, got {type(node)}")

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            INSERT INTO {self.schema}.nodes (
                id,
                type,
                name,
                canonical,
                metadata
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE SET
                type = EXCLUDED.type,
                name = EXCLUDED.name,
                canonical = EXCLUDED.canonical,
                metadata = EXCLUDED.metadata
            """,
            (
                node.id,
                node.type,
                node.name,
                node.canonical,
                json.dumps(node.metadata),
            ),
        )

    def get_node(self, node_id: str):

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM {self.schema}.nodes
            WHERE id = %s
            """,
            (node_id,),
        )

        return cursor.fetchone()

    # =====================================================
    # EDGE OPS
    # =====================================================

    def save_edge(self, edge: EdgeRecordV2):

        if not isinstance(edge, EdgeRecordV2):
            raise TypeError(f"Expected EdgeRecordV2, got {type(edge)}")

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            INSERT INTO {self.schema}.edges (
                id,
                source,
                target,
                type,
                layer,
                status,
                confidence,
                metadata
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE SET
                source = EXCLUDED.source,
                target = EXCLUDED.target,
                type = EXCLUDED.type,
                layer = EXCLUDED.layer,
                status = EXCLUDED.status,
                confidence = EXCLUDED.confidence,
                metadata = EXCLUDED.metadata
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

    def get_edges_from(self, node_id: str):

        cursor = self.conn.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM {self.schema}.edges
            WHERE source = %s
            """,
            (node_id,),
        )

        return cursor.fetchall()
