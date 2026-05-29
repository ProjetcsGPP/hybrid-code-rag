# pipeline_v2/tests/identity_contract/identity_test_fixtures.py


class FakeSymbol:

    def __init__(self, id, name, canonical):

        self.id = id
        self.name = name
        self.canonical = canonical


class FakeGraphNode:

    def __init__(self, node_id):

        self.id = node_id


class FakeIdentityRegistry:

    def __init__(self):

        self.by_id = {}
        self.by_canonical = {}

    def register(self, obj):

        self.by_id[obj.id] = obj

        canonical = getattr(obj, "canonical", None)

        if canonical:
            self.by_canonical[canonical] = obj

    def exists(self, node_id):

        return node_id in self.by_id


class FakeSymbolCore:

    def __init__(self, symbols):

        self._symbols = symbols

    def get_all_symbols(self):

        return self._symbols


class FakeGraph:

    def __init__(self):

        self.nodes = {}
        self.edges = {}


class FakeRelationshipCore:

    pass
