# pipeline_v2/validation/snapshots/deterministic_contract.py


class DeterministicValidationContract:

    def enforce(self, snapshot):

        return self._sanitize(snapshot)

    def _sanitize(self, snapshot):

        return snapshot.__class__(
            nodes=self._clean(snapshot.nodes),
            edges=self._clean(snapshot.edges),
            registry=self._clean(snapshot.registry),
            chunks=self._clean(snapshot.chunks),
            symbols=self._clean(snapshot.symbols),
            relationships=self._clean(snapshot.relationships),
            project_root=snapshot.project_root,
        )

    def _clean(self, data):

        # 🔥 remove qualquer objeto não serializável
        if isinstance(data, dict):
            return {str(k): self._clean(v) for k, v in data.items()}

        if isinstance(data, list):
            return [self._clean(x) for x in data]

        if hasattr(data, "__dict__"):
            return str(data)

        return data
