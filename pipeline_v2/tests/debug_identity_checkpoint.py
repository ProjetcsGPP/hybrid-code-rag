# pipeline_v2/tests/debug_identity_checkpoint.py

from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2

registry = IdentityRegistryV2()


class MockSymbol:
    def __init__(self, id, name, canonical):
        self.id = id
        self.name = name
        self.canonical = canonical


# Setup
s1 = MockSymbol("symbol_1", "some_symbol", "file.py.some_symbol")
registry.register(s1)

print("\n--- STATS ---")
print(registry.stats())

print("\n--- DIRECT ---")
print(registry.resolve("symbol_1"))

print("\n--- NAME ---")
print(registry.resolve("some_symbol"))

print("\n--- UNKNOWN ---")
print(registry.resolve("unknown_symbol"))
