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

        self.inheritance_index: Dict[str, List[str]] = {}

    # ---------------------------------------------------------
    # ADD
    # ---------------------------------------------------------

    def add(self, symbol: Symbol):

        print("\nINDEX ADD:")
        print("SYMBOL:", symbol.symbol_id)
        print("PARENT:", symbol.parent_symbol_id)

        # PRIMARY STORAGE
        self.by_id[symbol.symbol_id] = symbol

        # INHERITANCE INDEX

        if symbol.symbol_type == "class" and symbol.bases:

            for base in symbol.bases:

                self.add_inheritance(
                    symbol.symbol_id,
                    base,
                )

        # NAME INDEX
        self.by_name.setdefault(symbol.name, []).append(symbol)

        # MODULE INDEX
        self.by_module.setdefault(symbol.module_name, []).append(symbol)

        # CLASS INDEX
        if symbol.parent_symbol_id:

            print("ADDING TO CLASS INDEX")

            print("\nCLASS INDEX ADD")
            print("KEY:", symbol.parent_symbol_id)
            print("VALUE:", symbol.symbol_id)

            self.by_class.setdefault(symbol.parent_symbol_id, []).append(symbol)

        # CANONICAL INDEX
        self.by_canonical_name[symbol.canonical_name] = symbol

    def add_inheritance(
        self,
        child_class_id: str,
        base_class_name: str,
    ):

        print("\nADD INHERITANCE")
        print("CHILD:", child_class_id)
        print("BASE:", base_class_name)

        self.inheritance_index.setdefault(child_class_id, []).append(base_class_name)

    # ---------------------------------------------------------
    # GETTERS
    # ---------------------------------------------------------

    def get(self, symbol_id: str):

        return self.by_id.get(symbol_id)

    def get_by_name(self, name: str):

        return self.by_name.get(name, [])

    def get_by_id_suffix(self, suffix: str):

        for sid, sym in self.by_id.items():

            if sid.endswith(suffix):
                return sym

        return None

    def get_by_canonical_name(
        self,
        canonical_name: str,
    ):

        return self.by_canonical_name.get(canonical_name)

    def get_module_symbols(
        self,
        module_name: str,
    ):

        return self.by_module.get(module_name, [])

    def get_class_symbols(
        self,
        class_symbol_id: str,
    ):

        print("\nCLASS INDEX GET")
        print("SEARCH KEY:", class_symbol_id)

        print("AVAILABLE KEYS:", list(self.by_class.keys()))

        return self.by_class.get(class_symbol_id, [])

    def resolve_class_by_name(self, name: str):
        # 1. canonical match
        sym = self.by_canonical_name.get(name)
        if sym:
            return sym

        # 2. fallback name match (class only)
        candidates = self.by_name.get(name, [])
        for c in candidates:
            if c.symbol_type == "class":
                return c

        return None

    def resolve_framework_method(self, base_name, method_name):

        if base_name != "models.Model":
            return None

        DJANGO_MODEL_METHODS = {
            "save",
            "delete",
            "full_clean",
            "clean",
            "refresh_from_db",
            "validate_unique",
        }

        if method_name in DJANGO_MODEL_METHODS:
            return Symbol(
                symbol_id=f"django.db.models.Model::{method_name}",
                symbol_path="django.db.models.Model",
                canonical_name=f"django.db.models.Model.{method_name}",
                name=method_name,
                symbol_type="framework_method",
                module_name="django.db.models",
                file_path="django_builtin",
                parent_symbol_id="django.db.models.Model",
                semantic_type="framework",
                start_line=0,
                end_line=0,
                calls=[],
                imports=[],
                bases=[],
            )

        return None

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    def find_method_in_class(
        self,
        class_symbol_id: str,
        method_name: str,
    ):

        print("\nFIND METHOD IN CLASS")
        print("CLASS ID:", class_symbol_id)
        print("METHOD:", method_name)

        print("\nAVAILABLE CLASS KEYS:")
        for k in self.by_class.keys():
            print("-", k)

        methods = self.by_class.get(class_symbol_id, [])

        print("\nFOUND METHODS:")
        for m in methods:
            print("-", m.symbol_id)

        for method in methods:

            if method.name == method_name:

                print("MATCH FOUND:", method.symbol_id)

                return method

        print("NO MATCH")

        return None

    def find_local_function(
        self,
        module_name: str,
        function_name: str,
    ):

        symbols = self.by_module.get(module_name, [])

        for symbol in symbols:

            if symbol.symbol_type != "function":
                continue

            # ignora métodos
            if symbol.parent_symbol_id:
                continue

            if symbol.name == function_name:
                return symbol

        return None

    def find_method_in_hierarchy(
        self,
        class_symbol_id: str,
        method_name: str,
        visited=None,
    ):

        if visited is None:
            visited = set()

        if class_symbol_id in visited:
            return None

        visited.add(class_symbol_id)

        # -----------------------------------------
        # LOCAL CLASS
        # -----------------------------------------

        local = self.find_method_in_class(
            class_symbol_id,
            method_name,
        )

        if local:
            return local

        # -----------------------------------------
        # BASE CLASSES
        # -----------------------------------------

        bases = self.inheritance_index.get(class_symbol_id, [])

        print("\nHIERARCHY SEARCH")
        print("CLASS:", class_symbol_id)
        print("BASES:", bases)

        for base_name in bases:

            # -----------------------------------------
            # DJANGO / FRAMEWORK FAST PATH
            # -----------------------------------------

            framework_match = self.resolve_framework_method(
                base_name,
                method_name,
            )

            if framework_match:
                print("find_method_in_hierarchy.framework_match:", framework_match)
                return framework_match

            # -----------------------------------------
            # LOCAL BASE CLASS
            # -----------------------------------------

            base_symbol = self.get_by_canonical_name(base_name)

            if base_symbol is None:
                print("find_method_in_hierarchy.get_by_canonical_name.base_symbol none")
                continue

            found = self.find_method_in_hierarchy(
                base_symbol.symbol_id,
                method_name,
                visited,
            )

            if found:
                return found

        return None

    def search(self, name: str):

        return self.by_name.get(name, [])
