# pipeline/structure/relationship_extractor.py

from pipeline.contracts import Relationship, Symbol
from pipeline.structure.resolver.symbol_index import SymbolIndex
from pipeline.structure.models.callsite import CallSite
from pipeline.structure.resolver.symbol_resolver import SymbolResolver
from pipeline.structure.resolver.call_normalizer import CallNormalizer

from pipeline.structure.resolver.semantic_call_resolver import SemanticCallResolver
from pipeline.structure.resolver.semantic_call import SemanticCallTarget


class RelationshipExtractor:

    def __init__(self, symbol_index):
        self.normalizer = CallNormalizer()
        self.semantic_resolver = SemanticCallResolver(symbol_index)

    def _map_edge_type(self, call_type: str):

        if call_type == "SELF_METHOD":
            return "CALLS_SELF"

        if call_type == "SUPER_METHOD":
            return "CALLS_SUPER"

        if call_type in ("ORM_MANAGER", "django_manager"):
            return "CALLS_ORM"

        if call_type == "EXTERNAL":
            return "CALLS_EXTERNAL"

        return "CALLS_METHOD"

    def extract(
        self,
        symbol: Symbol,
        symbol_index: SymbolIndex,
        resolver: SymbolResolver,
    ) -> list[Relationship]:

        relationships: list[Relationship] = []

        # ---------------------------
        # BELONGS_TO
        # ---------------------------
        if symbol.parent_symbol_id:
            relationships.append(
                Relationship(
                    relationship_id=f"belongs_to::{symbol.symbol_id}::{symbol.parent_symbol_id}",
                    source_symbol_id=symbol.symbol_id,
                    target_symbol_id=symbol.parent_symbol_id,
                    relationship_type="BELONGS_TO",
                )
            )

        # ---------------------------
        # CALLS
        # ---------------------------
        if symbol.calls:

            for call in symbol.calls:

                # ✅ NORMALIZAÇÃO CENTRALIZADA
                normalized = self.normalizer.normalize(call, symbol)

                if not normalized:
                    continue

                callsite = self.build_callsite(normalized)

                semantic = self.semantic_resolver.resolve(
                    callsite,
                    symbol
                )

                target = semantic.resolved_symbol

                # -----------------------------------
                # UNRESOLVED EDGE (NÃO DESCARTA)
                # -----------------------------------

                if not target:

                    relationships.append(
                        Relationship(
                            relationship_id=(
                                f"calls::{symbol.symbol_id}"
                                f"::unresolved::{normalized}"
                            ),
                            source_symbol_id=symbol.symbol_id,
                            target_symbol_id=None,
                            relationship_type="CALLS_UNRESOLVED",
                            confidence=0.2,
                        )
                    )

                    continue

                # -----------------------------------
                # SELF LOOP
                # -----------------------------------

                if target.symbol_id == symbol.symbol_id:
                    continue

                # -----------------------------------
                # DJANGO NOISE FILTER
                # -----------------------------------

                if target.symbol_path.startswith("models."):
                    continue

                edge_type = self._map_edge_type(
                    semantic.call_type
                )

                relationships.append(
                    Relationship(
                        relationship_id=(
                            f"calls::{symbol.symbol_id}"
                            f"::{target.symbol_id}"
                        ),
                        source_symbol_id=symbol.symbol_id,
                        target_symbol_id=target.symbol_id,
                        relationship_type=edge_type,
                        confidence=semantic.confidence,
                    )
                )                

        return relationships

    def build_callsite(self, raw: str) -> CallSite:

        parts = raw.split(".")

        if len(parts) == 1:
            return CallSite(
                raw=raw,
                owner=None,
                method=parts[0],
                chain=[],
                call_type="function"
            )

        owner = parts[0]
        method = parts[-1]
        chain = parts[1:]

        if owner == "self":
            return CallSite(
                raw=raw,
                owner=owner,
                method=method,
                chain=chain,
                call_type="self_method"
            )

        if owner == "super":
            return CallSite(
                raw=raw,
                owner=owner,
                method=method,
                chain=chain,
                call_type="super_method"
            )
            
        if "objects" in parts:
            return CallSite(
                raw=raw,
                owner=owner,
                method=method,
                chain=chain,
                call_type="django_manager"
            )

        return CallSite(
            raw=raw,
            owner=owner,
            method=method,
            chain=chain,
            call_type="method"
        )