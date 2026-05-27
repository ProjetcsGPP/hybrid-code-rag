# pipeline_v2/core/identity/identity_reader_v1.py


class IdentityReaderV1:

    def __init__(self, identity_registry):
        self.registry = identity_registry

    def iter_symbols(self):
        for obj in self.registry.by_id.values():
            if (
                hasattr(obj, "name")
                and hasattr(obj, "canonical")
                and hasattr(obj, "type")
            ):
                yield obj

    def iter_relationships(self):
        for obj in self.registry.by_id.values():
            if hasattr(obj, "source") and hasattr(obj, "target"):
                yield obj

    def iter_nodes(self):
        for obj in self.registry.by_id.values():
            if (
                hasattr(obj, "name")
                and hasattr(obj, "canonical")
                and hasattr(obj, "metadata")
            ):
                # GraphNodeV2 também passa aqui, mas pode filtrar depois se quiser
                yield obj
