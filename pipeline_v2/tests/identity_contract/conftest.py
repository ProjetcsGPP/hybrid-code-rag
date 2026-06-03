# pipeline_v2/tests/identity_contract/conftest.py

import pytest

from pipeline_v2.tests.identity_contract.identity_test_fixtures import (
    FakeIdentityRegistry,
    FakeSymbol,
    FakeSymbolCore,
    FakeGraph,
    FakeRelationshipCore,
)


@pytest.fixture
def identity_registry():

    registry = FakeIdentityRegistry()

    s1 = FakeSymbol(
        "symbol_1",
        "some_symbol",
        "file.py.some_symbol",
    )

    registry.register(s1)

    return registry


@pytest.fixture
def symbol_core(identity_registry):

    return FakeSymbolCore(list(identity_registry.by_id.values()))


@pytest.fixture
def graph(identity_registry):

    graph = FakeGraph()

    graph.nodes["symbol_1"] = identity_registry.by_id["symbol_1"]

    return graph


@pytest.fixture
def relationship_core():

    return FakeRelationshipCore()
