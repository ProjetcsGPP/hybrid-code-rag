# pipeline_v2/core/identity/identity_gateway.py


class IdentityGatewayV2:

    def __init__(self, registry):
        self.registry = registry

    def register_symbol(self, symbol):
        return self.registry.register(symbol)

    def register_relationship(self, rel):
        return self.registry.register(rel)

    def resolve(self, obj_id):
        return self.registry.resolve_id(obj_id)
