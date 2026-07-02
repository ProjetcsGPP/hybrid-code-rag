# pipeline_v2/tests/validation/conftest.py


import pytest
from pipeline_v2.validation.snapshots.snapshot_engine import ValidationSnapshotEngineV3

# -------------------------
# Stubs consistentes V3
# -------------------------


class DummyGraphCore:
    def __init__(self):
        self.nodes_data = {
            "n1": {},
            "n2": {},
        }
        self.edges_data = {
            "e1": {},
        }

    def get_nodes(self):
        return self.nodes_data

    def get_edges(self):
        return self.edges_data


class DummyRegistry:
    pass


class ValidationContext:
    def __init__(self):
        self.project_root = "/tmp"
        self.runtime = None
        self.identity_registry = DummyRegistry()

        self.graph_core = DummyGraphCore()

        self.chunks = [
            {"id": "n1", "type": "symbol"},
            {"id": "n2", "type": "chunk"},
        ]

        self.symbols = [{"id": "s1"}]
        self.relationships = [
            {"id": "e1", "source": "n1", "target": "n2", "type": "relates"}
        ]


class SnapshotEngineStub(ValidationSnapshotEngineV3):
    pass


# -------------------------
# Fixtures
# -------------------------


@pytest.fixture
def context():
    return ValidationContext()


@pytest.fixture
def snapshot_engine():
    return SnapshotEngineStub()


@pytest.fixture
def snapshot(snapshot_engine, context):
    return snapshot_engine.build(context)


# Pipeline stub simples (para teste de estabilidade)
@pytest.fixture
def run_pipeline():
    def _run():
        return {
            "graph_nodes": {"n1": 1, "n2": 2},
            "chunks": [{"id": "c1"}, {"id": "c2"}],
        }

    return _run
