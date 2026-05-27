# pipeline_v2/core/identity/identity_service_v2.py


class IdentityServiceV2:

    def __init__(self, registry):
        self.registry = registry

    def resolve(self, obj):
        if hasattr(obj, "id"):
            return self.registry.resolve_id(obj.id)
        return str(obj)

    def register(self, obj):
        return self.registry.register(obj)
