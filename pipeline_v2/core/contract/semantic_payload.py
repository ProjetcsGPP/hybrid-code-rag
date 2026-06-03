# pipeline_v2/core/contract/semantic_payload.py


class SemanticPayload:
    """
    Contrato intermediário entre Legacy e V2.
    """

    def __init__(self, symbols, inheritance_edges, calls, imports):
        self.symbols = symbols
        self.inheritance_edges = inheritance_edges
        self.calls = calls
        self.imports = imports
