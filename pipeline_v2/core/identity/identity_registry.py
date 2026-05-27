# pipeline_v2/core/identity/identity_registry.py


class IdentityRegistryV2:
    """
    Single source of truth for all IDs:
    - symbols
    - nodes
    - edges
    """

    def __init__(self):
        self.by_name = {}
        self.by_id = {}

    def register(self, obj):

        obj_id = getattr(obj, "id", None)
        name = getattr(obj, "name", None)

        if obj_id:
            self.by_id[obj_id] = obj

        if name:
            self.by_name[name] = obj

        return obj

    def resolve_name(self, name: str):
        obj = self.by_name.get(name)
        return obj.id if obj else None

    def resolve_id(self, obj_id: str):
        return self.by_id.get(obj_id)
