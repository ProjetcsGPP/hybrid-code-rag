# pipeline_v2/core/symbol/symbol_index.py


class SymbolIndexV2:

    def __init__(self, identity_registry):
        self.by_id = {}
        self.by_name = {}
        self.by_file = {}
        self.by_canonical = {}

        self.identity_registry = identity_registry

    def add(self, symbol):

        self.by_id[symbol.id] = symbol

        self.by_name.setdefault(
            symbol.name,
            [],
        ).append(symbol.id)

        self.by_file.setdefault(
            symbol.file_path,
            [],
        ).append(symbol.id)

        self.by_canonical.setdefault(
            symbol.canonical,
            [],
        ).append(symbol.id)

    def get(self, symbol_id: str):

        return self.by_id.get(symbol_id)

    def find_by_name(self, name: str):

        return self.identity_registry.resolve_by_name(name)

    def find_by_canonical(self, canonical: str):

        return self.identity_registry.resolve_by_canonical(canonical)
