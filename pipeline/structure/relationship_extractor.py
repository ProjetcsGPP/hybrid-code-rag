# pipeline/structure/relationship_extractor.py

from pipeline.contracts import Relationship, Symbol
from pipeline.structure.resolver.symbol_index import SymbolIndex


class RelationshipExtractor:

    def extract(self, symbol: Symbol, symbol_index: SymbolIndex) -> list[Relationship]:

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

                # -----------------------------------
                # IGNORA CALLS EXTERNAS / FRAMEWORK
                # -----------------------------------

                if "." in call:

                    root = call.split(".")[0]

                    ignored_roots = {
                        "self",
                        "super",
                        "objects",
                        "models",
                        "timezone",
                        "settings",
                    }

                    if root in ignored_roots:
                        continue

                target = symbol_index.resolve_best(call, context=symbol)

                if not target:
                    continue

                if target.symbol_id == symbol.symbol_id:
                    continue

                relationships.append(
                    Relationship(
                        relationship_id=f"calls::{symbol.symbol_id}::{target.symbol_id}",
                        source_symbol_id=symbol.symbol_id,
                        target_symbol_id=target.symbol_id,
                        relationship_type="CALLS",
                        confidence=0.85,
                    )
                )

        return relationships