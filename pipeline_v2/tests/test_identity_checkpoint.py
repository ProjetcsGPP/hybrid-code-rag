# pipeline_v2/tests/test_identity_checkpoint.py


from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2


def build_sample_registry():
    registry = IdentityRegistryV2()

    # Simula registros reais do pipeline
    class MockSymbol:
        def __init__(self, id, name, canonical):
            self.id = id
            self.name = name
            self.canonical = canonical

    s1 = MockSymbol("symbol_1", "some_symbol", "file.py.some_symbol")
    s2 = MockSymbol("symbol_2", "another_symbol", "file.py.another_symbol")

    registry.register(s1)
    registry.register(s2)

    return registry


def test_stats():
    registry = build_sample_registry()

    stats = registry.stats()
    print("STATS:", stats)

    assert stats["ids"] == 2
    assert stats["names"] >= 2
    assert stats["canonicals"] == 2


def test_resolve_direct():
    registry = build_sample_registry()

    result = registry.resolve("symbol_1")
    print("DIRECT:", result)

    assert result == "symbol_1"


def test_resolve_by_name():
    registry = build_sample_registry()

    result = registry.resolve("some_symbol")
    print("NAME:", result)

    assert result == "symbol_1"


def test_resolve_external():
    registry = build_sample_registry()

    result = registry.resolve("unknown_symbol")
    print("EXTERNAL:", result)

    assert result == "external::unknown_symbol"
