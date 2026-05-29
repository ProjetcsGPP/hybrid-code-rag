# pipeline_v2/tests/debug_identity_raw.py

from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2

registry = IdentityRegistryV2()


class Dummy:
    def __init__(self, id, name, canonical):
        self.id = id
        self.name = name
        self.canonical = canonical


a = Dummy("symbol_1", "test_symbol", "file.a")
b = Dummy("symbol_2", "another_symbol", "file.b")

registry.register(a)
registry.register(b)

print("IDS:", registry.by_id)
print("NAMES:", registry.by_name)
print("CANONICALS:", registry.by_canonical)
print("STATS:", registry.stats())
