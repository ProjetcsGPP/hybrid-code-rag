# pipeline_v2/validation/snapshots/snapshot_engine.py


class SnapshotSerializationError(Exception):
    pass


class ValidationSnapshotEngineV3:
    """
    Snapshot V3 estrito:
    - retorna dict puro
    - determinístico
    - sem objetos runtime
    - sem __dict__
    """

    def build(self, context):
        nodes = self._normalize_nodes(context.chunks)
        edges = self._normalize_edges(context.relationships)

        snapshot = {
            "nodes": nodes,
            "edges": edges,
            "registry": self._safe_registry(context),
            "metadata": {
                "version": "v3",
                "deterministic": True,
            },
            "project_root": context.project_root,
        }

        self._validate(snapshot)
        return snapshot

    # -------------------------
    # Normalização
    # -------------------------

    def _normalize_nodes(self, chunks):
        result = {}
        for i, c in enumerate(chunks):
            if not isinstance(c, dict):
                raise SnapshotSerializationError("Invalid node type")

            node_id = c.get("id", f"n{i}")
            result[node_id] = {
                "id": node_id,
                "type": c.get("type", "chunk"),
                **{k: v for k, v in c.items() if k != "id"},
            }
        return result

    def _normalize_edges(self, relationships):
        result = {}
        for i, r in enumerate(relationships):
            if not isinstance(r, dict):
                raise SnapshotSerializationError("Invalid edge type")

            edge_id = r.get("id", f"e{i}")
            result[edge_id] = {
                "id": edge_id,
                "source": r.get("source"),
                "target": r.get("target"),
                "type": r.get("type", "relates"),
            }
        return result

    def _safe_registry(self, context):
        return {} if context.identity_registry is None else {}

    # -------------------------
    # Validação estrita
    # -------------------------

    def _validate(self, snapshot):
        # nodes/edges obrigatórios
        if "nodes" not in snapshot or "edges" not in snapshot:
            raise SnapshotSerializationError("Missing required fields")

        if not isinstance(snapshot["nodes"], dict):
            raise SnapshotSerializationError("nodes must be dict")

        if not isinstance(snapshot["edges"], dict):
            raise SnapshotSerializationError("edges must be dict")

        # rejeitar objetos Python soltos
        for v in snapshot["nodes"].values():
            if isinstance(v, object) and not isinstance(
                v, (str, int, float, dict, list)
            ):
                raise SnapshotSerializationError("Invalid object in nodes")
