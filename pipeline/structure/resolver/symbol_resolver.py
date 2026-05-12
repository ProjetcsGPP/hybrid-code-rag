# pipeline/structure/resolver/symbol_resolver.py

from pipeline.contracts import Symbol
from pipeline.structure.models.callsite import CallSite
from pipeline.structure.resolver.scoring import ResolutionScorer


class SymbolResolver:

    def __init__(self, symbol_index: "SymbolIndex"):
        self.index = symbol_index
        self.scorer = ResolutionScorer()

    def resolve_calls(
        self,
        calls: list[CallSite],
        context_symbol: Symbol
    ) -> list[Symbol]:

        resolved = []

        for call in calls:
            symbol = self._resolve_single(call, context_symbol)
            if symbol:
                resolved.append(symbol)

        return resolved

    def _resolve_single(self, call, context_symbol):

        search_name = None

        # -----------------------------
        # NORMALIZAÇÃO DA CHAMADA
        # -----------------------------
        if hasattr(call, "call_type"):

            if call.call_type == "self_method":
                search_name = call.method

            elif call.call_type == "super_method":
                search_name = call.method

            elif call.call_type == "django_manager":
                return None  # bloqueio total ORM

            else:
                search_name = call.raw

        else:
            search_name = call

        candidates = self.index.search(search_name)

        if not candidates:
            return None

        # -----------------------------
        # FILTRO DE RUÍDO GLOBAL
        # -----------------------------
        candidates = [
            c for c in candidates
            if not c.symbol_path.startswith("models.")
            and not c.module_name.startswith("django")
        ]

        if not candidates:
            return None

        # -----------------------------
        # BOOST HEURÍSTICO (NÃO SHORT-CIRCUIT)
        # -----------------------------
        boosts = {}

        for c in candidates:
            boosts[c.symbol_id] = 0.0

            # mesma classe
            if c.parent_symbol_id == context_symbol.parent_symbol_id:
                boosts[c.symbol_id] += 0.3

            # mesmo arquivo
            if c.file_path == context_symbol.file_path:
                boosts[c.symbol_id] += 0.2

            # mesmo módulo
            if c.module_name == context_symbol.module_name:
                boosts[c.symbol_id] += 0.1

        # -----------------------------
        # fallback cross-file boost
        # -----------------------------

        if candidates and context_symbol:

            for c in candidates:
                if c.module_name != context_symbol.module_name:
                    boosts[c.symbol_id] = max(
                        boosts[c.symbol_id] - 0.2,
                        -0.5
                    )
                    
        # -----------------------------
        # SCORING FINAL (ÁRBITRO)
        # -----------------------------
        scored = []

        for c in candidates:

            base_score = self.scorer.score(c, search_name, context_symbol)
            final_score = base_score + boosts.get(c.symbol_id, 0.0)

            scored.append((final_score, c))

        scored.sort(key=lambda x: x[0], reverse=True)

        return scored[0][1] if scored else None

    def explain(self, call: str):
        return {
            "call": call,
            "candidates": self.index.search(call)
        }