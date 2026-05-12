# pipeline/structure/structural_query.py

from pipeline.structure.storage.sqlite_store import SQLiteStructuralStore


class StructuralQuery:

    def __init__(self, store: SQLiteStructuralStore):
        self.store = store

    # ---------------------------------------------
    # SYMBOL QUERIES
    # ---------------------------------------------

    def get_symbol(self, symbol_id: str):
        return self.store.get_symbol(symbol_id)

    def get_symbols_by_name(self, name: str):

        cursor = self.store.conn.cursor()

        cursor.execute(
            """
            SELECT * FROM symbols
            WHERE name = ?
            """,
            (name,)
        )

        return cursor.fetchall()

    def get_symbols_by_file(self, file_path: str):

        cursor = self.store.conn.cursor()

        cursor.execute(
            """
            SELECT * FROM symbols
            WHERE file_path = ?
            """,
            (file_path,)
        )

        return cursor.fetchall()

    def get_children(self, parent_symbol_id: str):

        cursor = self.store.conn.cursor()

        cursor.execute(
            """
            SELECT * FROM symbols
            WHERE parent_symbol_id = ?
            """,
            (parent_symbol_id,)
        )

        return cursor.fetchall()

    # ---------------------------------------------
    # RELATIONSHIP QUERIES
    # ---------------------------------------------

    def get_relationships(self, symbol_id: str):

        return self.store.get_relationships(symbol_id)

    def get_relationships_by_type(
        self,
        symbol_id: str,
        relationship_type: str,
    ):

        cursor = self.store.conn.cursor()

        cursor.execute(
            """
            SELECT * FROM relationships
            WHERE (source_symbol_id = ? OR target_symbol_id = ?)
            AND relationship_type = ?
            """,
            (
                symbol_id,
                symbol_id,
                relationship_type,
            )
        )

        return cursor.fetchall()
    
    def get_parent(self, symbol_id: str):

        cursor = self.store.conn.cursor()

        cursor.execute(
            """
            SELECT parent_symbol_id
            FROM symbols
            WHERE symbol_id = ?
            """,
            (symbol_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        parent_id = row["parent_symbol_id"]

        if not parent_id:
            return None

        return self.get_symbol(parent_id)