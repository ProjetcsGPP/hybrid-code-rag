# pipeline_v2/core/symbols/symbol.py

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum


class SymbolType(str, Enum):
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    IMPORT = "import"
    MODULE = "module"


class ScopeType(str, Enum):
    GLOBAL = "global"
    CLASS = "class"
    FUNCTION = "function"
    BLOCK = "block"
    MODULE = "module"


@dataclass
class Symbol:
    """
    Symbol V2 - núcleo canônico do sistema semântico.

    Representa qualquer entidade identificável em código,
    independente de linguagem ou framework.
    """

    # identidade base
    id: str
    name: str
    symbol_type: SymbolType

    # localização no código
    file_path: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None

    # hierarquia semântica
    parent_id: Optional[str] = None
    scope: ScopeType = ScopeType.GLOBAL

    # linguagem/framework origem
    language: str = "python"
    framework: Optional[str] = None  # django, react, nextjs etc

    # metadados estruturais
    canonical_path: Optional[str] = None
    qualified_name: Optional[str] = None

    # propriedades extras (extensível para Next.js, TS, etc)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # relações futuras (grafo)
    calls: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)

    def is_method(self) -> bool:
        return self.symbol_type == SymbolType.METHOD

    def is_class(self) -> bool:
        return self.symbol_type == SymbolType.CLASS

    def is_function(self) -> bool:
        return self.symbol_type == SymbolType.FUNCTION

    def add_call(self, target_symbol_id: str):
        if target_symbol_id not in self.calls:
            self.calls.append(target_symbol_id)

    def add_reference(self, target_symbol_id: str):
        if target_symbol_id not in self.references:
            self.references.append(target_symbol_id)
