# pipeline_v2/core/symbol/symbol_core.py

from .symbol_index import SymbolIndexV2
from .symbol_factory import SymbolFactoryV2
from .symbol_types import SymbolType


class SymbolCoreV2:

    def __init__(self):
        self.index = SymbolIndexV2()

    def create_symbol(self, name: str, type: SymbolType, file_path: str, **kwargs):
        symbol = SymbolFactoryV2.create(
            name=name, type=type, file_path=file_path, **kwargs
        )

        self.index.add(symbol)
        return symbol

    def get_symbol(self, symbol_id: str):
        return self.index.get(symbol_id)

    def find_by_name(self, name: str):
        return self.index.find_by_name(name)
