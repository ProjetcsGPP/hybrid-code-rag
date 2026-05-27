# pipeline_v2/tests/identity_contract/identity_test_fixtures.py


class FakeSymbol:
    def __init__(self, name, canonical_id):
        self.name = name
        self.canonical_id = canonical_id


class FakeGraphNode:
    def __init__(self, node_id):
        self.id = node_id


class FakeIdentityRegistry:

    def __init__(self, mapping):
        self.mapping = mapping

    def resolve(self, name):
        return self.mapping.get(name)

    def exists(self, node_id):
        return node_id in self.mapping.values()


class FakeSymbolCore:

    def __init__(self, symbols):
        self._symbols = symbols

    def get_all_symbols(self):
        return self._symbols


class FakeGraph:

    def __init__(self, nodes):
        self._nodes = nodes

    def get_nodes(self):
        return self._nodes


class FakeRelationshipCore:

    def __init__(self, calls):
        self._calls = calls

    def get_internal_calls(self):
        return self._calls
