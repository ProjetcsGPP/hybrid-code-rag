# pipeline/structure/resolver/symbol_index.py

from typing import Dict, List
from pipeline.contracts import Symbol


class SymbolIndex:

    def __init__(self):
        self.by_id: Dict[str, Symbol] = {}
        self.by_name: Dict[str, List[Symbol]] = {}

    def add(self, symbol: Symbol):
        self.by_id[symbol.symbol_id] = symbol

        self.by_name.setdefault(symbol.name, []).append(symbol)

    def get(self, symbol_id: str):
        return self.by_id.get(symbol_id)

    def get_by_name(self, name: str):
        return self.by_name.get(name, [None])[0]

    def get_by_id_suffix(self, suffix: str):
        for sid, sym in self.by_id.items():
            if sid.endswith(suffix):
                return sym
        return None

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
