# pipeline_v2/core/symbols/symbol_index.py

from typing import Dict, List, Optional
from .symbol import Symbol


class SymbolIndex:
    """
    Índice global de símbolos V2.

    Responsável por:
    - lookup por id
    - lookup por nome qualificado
    - agrupamento por arquivo
    """

    def __init__(self):
        self.by_id: Dict[str, Symbol] = {}
        self.by_file: Dict[str, List[str]] = {}
        self.by_name: Dict[str, List[str]] = {}

    def add(self, symbol: Symbol):
        self.by_id[symbol.id] = symbol

        # file index
        self.by_file.setdefault(symbol.file_path, []).append(symbol.id)

        # name index
        self.by_name.setdefault(symbol.name, []).append(symbol.id)

    def get(self, symbol_id: str) -> Optional[Symbol]:
        return self.by_id.get(symbol_id)

    def get_by_file(self, file_path: str) -> List[Symbol]:
        return [self.by_id[sid] for sid in self.by_file.get(file_path, [])]

    def find_by_name(self, name: str) -> List[Symbol]:
        return [self.by_id[sid] for sid in self.by_name.get(name, [])]

    def all(self) -> List[Symbol]:
        return list(self.by_id.values())
