# pipeline/structure/resolver/symbol_index.py

from typing import Dict, List
from pipeline.contracts import Symbol


class SymbolIndex:

    def __init__(self):
        self.by_id: Dict[str, Symbol] = {}

        self.by_name: Dict[str, List[Symbol]] = {}

        self.by_module: Dict[str, List[Symbol]] = {}

        self.by_class: Dict[str, List[Symbol]] = {}

        self.by_canonical_name: Dict[str, Symbol] = {}

    def add(self, symbol: Symbol):

        # -----------------------------------
        # PRIMARY STORAGE
        # -----------------------------------

        self.by_id[symbol.symbol_id] = symbol

        # -----------------------------------
        # NAME INDEX
        # -----------------------------------

        self.by_name.setdefault(
            symbol.name,
            []
        ).append(symbol)

        # -----------------------------------
        # MODULE INDEX
        # -----------------------------------

        self.by_module.setdefault(
            symbol.module_name,
            []
        ).append(symbol)

        # -----------------------------------
        # CLASS INDEX
        # -----------------------------------

        if symbol.parent_symbol_id:

            self.by_class.setdefault(
                symbol.parent_symbol_id,
                []
            ).append(symbol)

        # -----------------------------------
        # CANONICAL INDEX
        # -----------------------------------

        self.by_canonical_name[
            symbol.canonical_name
        ] = symbol

    def get(self, symbol_id: str):
        return self.by_id.get(symbol_id)

    def get_by_name(self, name: str):
        return self.by_name.get(name, [None])[0]

    def get_by_id_suffix(self, suffix: str):
        for sid, sym in self.by_id.items():
            if sid.endswith(suffix):
                return sym
        return None

    def get_by_canonical_name(
        self,
        canonical_name: str,
    ):
        return self.by_canonical_name.get(
            canonical_name
        )

    def get_module_symbols(
        self,
        module_name: str,
    ):
        return self.by_module.get(
            module_name,
            []
        )

    def get_class_symbols(
        self,
        class_symbol_id: str,
    ):
        return self.by_class.get(
            class_symbol_id,
            []
        )

    def resolve_best(self, call: str, context=None):
        candidates = self.by_name.get(call, [])

        if not candidates:
            return None

        if len(candidates) == 1:
            return candidates[0]

        # 🎯 prioridade 1: mesmo arquivo
        if context:
            same_file = [
                c for c in candidates
                if c.file_path == context.file_path
            ]
            if same_file:
                return same_file[0]

        # 🎯 prioridade 2: mesmo módulo
        if context:
            same_module = [
                c for c in candidates
                if c.module_name == context.module_name
            ]
            if same_module:
                return same_module[0]

        # fallback: primeiro mesmo
        return candidates[0]

    def search(self, name: str):
        return self.by_name.get(name, [])
