# pipeline_v2/core/symbol/symbol_core.py

from .symbol_factory import SymbolFactoryV2
from .symbol_types import SymbolType


from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2


class SymbolCoreV2:

    def __init__(self, identity_registry=None):

        # 🔥 SINGLE SOURCE OF TRUTH
        self.identity_registry = identity_registry or IdentityRegistryV2()

    # =====================================================
    # SYMBOL CREATION
    # =====================================================

    def create_symbol(
        self,
        name: str,
        type: SymbolType,
        file_path: str,
        **kwargs,
    ):

        symbol = SymbolFactoryV2.create(
            name=name,
            type=type,
            file_path=file_path,
            **kwargs,
        )

        # 🔥 ONLY ONE REGISTRY
        self.identity_registry.register(symbol)

        return symbol

    # =====================================================
    # LOOKUP (delegation only)
    # =====================================================

    def get_symbol(self, symbol_id: str):
        return self.identity_registry.resolve_id(symbol_id)

    def find_by_name(self, name: str):
        return self.identity_registry.resolve_by_name(name)

    def find_by_canonical(self, canonical: str):
        return self.identity_registry.resolve_by_canonical(canonical)

    # =====================================================
    # BULK ACCESS
    # =====================================================

    def get_all_symbols(self):
        return list(self.identity_registry.by_id.values())

    def clear_indexes(self):
        self._by_id.clear()
        self._by_canonical.clear()
        self._by_name.clear()
