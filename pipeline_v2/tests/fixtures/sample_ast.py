# pipeline_v2/tests/fixtures/sample_ast.py


def load_sample_ast():

    return {
        "id": "chunk_001",
        "file": "example.py",
        "metadata": {
            "chunk_id": "chunk_001",
            "file": "example.py",
            "symbol_path": "example.module",
            "calls": ["service.process", "repo.save"],
            "assignments": [],
        },
        "raw_calls": ["service.process", "repo.save"],
        "assignments": [],
    }
