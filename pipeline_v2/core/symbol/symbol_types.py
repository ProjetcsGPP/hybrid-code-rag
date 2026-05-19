# pipeline_v2/core/symbol/symbol_types.py

from enum import Enum


class SymbolType(str, Enum):
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    MODULE = "module"
