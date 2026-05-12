# pipeline/structure/graph/graph_store.py

class GraphStore:

    def __init__(self, sqlite_store):
        self.store = sqlite_store

    # -----------------------
    # NODE
    # -----------------------
    def save_node(self, symbol):

        self.store.save_symbol(symbol)

    # -----------------------
    # EDGE
    # -----------------------
    def save_edge(self, edge):

        self.store.save_relationship(edge)

    # -----------------------
    # BULK DEBUG OUTPUT
    # -----------------------
    def stats(self):

        cursor = self.store.conn.cursor()

        nodes = cursor.execute("SELECT COUNT(*) FROM symbols").fetchone()[0]

        edges = cursor.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]

        unresolved = cursor.execute("""
            SELECT COUNT(*) FROM relationships
            WHERE target_symbol_id IS NULL
        """).fetchone()[0]

        return {
            "nodes": nodes,
            "edges": edges,
            "unresolved": unresolved
        }