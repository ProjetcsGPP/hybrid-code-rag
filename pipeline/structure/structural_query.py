# pipeline/structure/structural_query.py
class StructuralQuery:

    def __init__(self, store):
        self.store = store

    # ---------------------------------------------
    # SYMBOL QUERIES
    # ---------------------------------------------

    def get_symbol(self, symbol_id: str):
        return self.store.get_symbol(symbol_id)

    def get_symbols_by_name(self, name: str):

        cursor = self.store.conn.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM {self.store.schema}.symbols
            WHERE name = %s
            """,
            (name,),
        )

        return cursor.fetchall()

    def get_symbols_by_file(self, file_path: str):

        cursor = self.store.conn.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM {self.store.schema}.symbols
            WHERE file_path = %s
            """,
            (file_path,),
        )

        return cursor.fetchall()

    def get_children(self, parent_symbol_id: str):

        cursor = self.store.conn.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM {self.store.schema}.symbols
            WHERE parent_symbol_id = %s
            """,
            (parent_symbol_id,),
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
            f"""
            SELECT *
            FROM {self.store.schema}.relationships
            WHERE (
                source_symbol_id = %s
                OR target_symbol_id = %s
            )
            AND relationship_type = %s
            """,
            (
                symbol_id,
                symbol_id,
                relationship_type,
            ),
        )

        return cursor.fetchall()

    def get_parent(self, symbol_id: str):

        cursor = self.store.conn.cursor()

        cursor.execute(
            f"""
            SELECT parent_symbol_id
            FROM {self.store.schema}.symbols
            WHERE symbol_id = %s
            """,
            (symbol_id,),
        )

        row = cursor.fetchone()

        if not row:
            return None

        parent_id = row["parent_symbol_id"]

        if not parent_id:
            return None

        return self.get_symbol(parent_id)
