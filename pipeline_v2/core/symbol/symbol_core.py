# pipeline_v2/core/symbol/symbol_core.py

from .symbol_index import SymbolIndexV2
from .symbol_factory import SymbolFactoryV2
from .symbol_types import SymbolType
from .symbol_models import SymbolV2

from pipeline_v2.core.identity.identity_registry import (
    IdentityRegistryV2,
)

from pipeline_v2.core.identity.identity_gateway import IdentityGatewayV2


class SymbolCoreV2:

    def __init__(
        self,
        identity_registry: IdentityRegistryV2 = None,
    ):

        self.index = SymbolIndexV2()

        self.identity_registry = identity_registry or IdentityRegistryV2()

        # 🔵 ADICIONAR GATEWAY (NOVO)
        self.identity = IdentityGatewayV2(self.identity_registry)

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

        self.index.add(symbol)

        # global identity registration
        self.identity.register_symbol(symbol)

        return symbol

    # =====================================================
    # LOOKUP
    # =====================================================

    def get_symbol(self, symbol_id: str):
        return self.index.get(symbol_id)

    def find_by_name(self, name: str):
        return self.index.find_by_name(name)

    def find_by_canonical(self, canonical: str):
        return self.index.find_by_canonical(canonical)

    # =====================================================
    # MANUAL REGISTRATION
    # =====================================================

    def register(self, symbol):

        self.index.add(symbol)

        self.identity.register_symbol(symbol)

        return symbol

    # =====================================================
    # CONTRACT LOADER
    # =====================================================

    @staticmethod
    def from_contract(contract):

        symbol_type = (
            contract.type
            if isinstance(contract.type, SymbolType)
            else SymbolType(contract.type)
        )

        return SymbolV2(
            id=contract.id,
            name=contract.name,
            type=symbol_type,
            file_path=contract.file_path,
            canonical=contract.canonical,
            parent=contract.parent,
            metadata=contract.metadata or {},
        )

    def get_all_symbols(self):
        """
        Contract method for inspection layers (tests, validation, debugging)
        Must return all registered symbols in the system.
        """

        if hasattr(self.index, "all"):
            return list(self.index.all())

        if hasattr(self.index, "values"):
            return list(self.index.values())

        if hasattr(self.index, "items"):
            return [v for _, v in self.index.items()]

        # fallback seguro (último caso)
        return list(getattr(self.index, "_symbols", {}).values())
