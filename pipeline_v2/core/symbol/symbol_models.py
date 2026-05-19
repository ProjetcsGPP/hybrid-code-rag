# pipeline_v2/core/symbol/symbol_models.py

from dataclasses import dataclass, field
from typing import Dict, Optional, List
from .symbol_types import SymbolType


@dataclass
class SymbolV2:
    id: str
    name: str
    type: SymbolType

    file_path: str
    canonical: str

    parent: Optional[str] = None

    bases: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)
