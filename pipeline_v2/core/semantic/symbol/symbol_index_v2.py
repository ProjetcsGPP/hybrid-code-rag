# pipeline_v2/core/semantic/symbol/symbol_index_v2.py

from collections import defaultdict

from .semantic_symbol import SemanticSymbol


class SymbolIndexV2:
    """
    Semantic Symbol Index.

    Responsável por:
    - canonical lookup
    - alias lookup
    - import lookup
    - inheritance lookup
    - framework lookup
    """

    def __init__(self):

        self.by_name = {}

        self.by_alias = {}

        self.by_canonical = {}

        self.by_import = {}

        self.by_framework = defaultdict(list)

        self.by_inheritance = defaultdict(list)

    # =====================================================
    # REGISTER
    # =====================================================

    def register(self, symbol: SemanticSymbol):

        self.by_name[symbol.canonical] = symbol

        self.by_canonical[symbol.canonical] = symbol

        # ---------------------------------------------
        # aliases
        # ---------------------------------------------

        for alias in symbol.aliases:
            self.by_alias[alias] = symbol

        # ---------------------------------------------
        # imports
        # ---------------------------------------------

        for imp in symbol.imports:
            self.by_import[imp] = symbol

        # ---------------------------------------------
        # framework
        # ---------------------------------------------

        if symbol.framework:
            self.by_framework[symbol.framework].append(symbol)

        # ---------------------------------------------
        # inheritance
        # ---------------------------------------------

        for base in symbol.inheritance_chain:
            self.by_inheritance[base].append(symbol)

    # =====================================================
    # LOOKUPS
    # =====================================================

    def resolve(self, canonical: str):

        return self.by_canonical.get(canonical)

    def resolve_alias(self, alias: str):

        return self.by_alias.get(alias)

    def resolve_import(self, import_path: str):

        return self.by_import.get(import_path)

    def resolve_canonical(self, canonical: str):

        return self.by_canonical.get(canonical)

    def resolve_inheritance(self, base_name: str):

        return self.by_inheritance.get(base_name, [])

    def resolve_framework(self, framework_name: str):

        return self.by_framework.get(framework_name, [])

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(self, canonical: str) -> bool:

        return canonical in self.by_canonical

    # =====================================================
    # DEBUG
    # =====================================================

    def stats(self):

        return {
            "canonical": len(self.by_canonical),
            "aliases": len(self.by_alias),
            "imports": len(self.by_import),
            "frameworks": len(self.by_framework),
            "inheritance": len(self.by_inheritance),
        }
