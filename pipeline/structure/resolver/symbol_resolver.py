from pipeline.contracts import Symbol


class SymbolResolver:

    def __init__(self, symbol_index: "SymbolIndex"):
        self.index = symbol_index

    def resolve_calls(self, calls: list[str], context_symbol: Symbol) -> list[Symbol]:

        resolved = []

        for call in calls:
            symbol = self._resolve_single(call, context_symbol)
            if symbol:
                resolved.append(symbol)

        return resolved

    def _resolve_single(self, call: str, context_symbol: Symbol):

        # -------------------------
        # 1. LOCAL CLASS SCOPE (PRIORIDADE MÁXIMA)
        # -------------------------
        if context_symbol.parent_symbol_id:
            parent = self.index.get(context_symbol.parent_symbol_id)

            if parent:
                candidates = self.index.search(call)

                same_class = [
                    c for c in candidates
                    if c.parent_symbol_id == parent.symbol_id
                ]
                if same_class:
                    return same_class[0]

        # -------------------------
        # 2. MESMO ARQUIVO
        # -------------------------
        candidates = self.index.search(call)

        same_file = [
            c for c in candidates
            if c.file_path == context_symbol.file_path
        ]
        if same_file:
            return same_file[0]

        # -------------------------
        # 3. MESMO MÓDULO
        # -------------------------
        same_module = [
            c for c in candidates
            if c.module_name == context_symbol.module_name
        ]
        if same_module:
            return same_module[0]

        # -------------------------
        # 4. FALLBACK GLOBAL
        # -------------------------
        return candidates[0] if candidates else None

    def explain(self, call: str):
        return {
            "call": call,
            "candidates": self.index.search(call)
        }