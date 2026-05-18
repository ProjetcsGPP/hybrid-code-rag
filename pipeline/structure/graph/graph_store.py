# pipeline/structure/graph/graph_store.py

from pipeline.contracts import Symbol


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
    # EXTERNAL NODE
    # -----------------------

    def ensure_external_node(
        self,
        owner: str | None,
        name: str,
    ):

        owner = owner or "external"

        symbol_id = f"external::{owner}::{name}"

        existing = self.store.get_symbol(symbol_id)

        if existing:

            return symbol_id

        external_symbol = Symbol(
            symbol_id=symbol_id,
            symbol_path=symbol_id,
            canonical_name=(f"{owner}.{name}"),
            name=name,
            symbol_type="external",
            module_name=owner,
            file_path="<external>",
            parent_symbol_id=None,
            semantic_type="external",
            start_line=0,
            end_line=0,
            calls=[],
            imports=[],
        )

        self.store.save_symbol(external_symbol)

        return symbol_id

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

        return {"nodes": nodes, "edges": edges, "unresolved": unresolved}
