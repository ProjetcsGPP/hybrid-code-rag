# pipeline_v2/core/builder/build_context.py

from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class BuildContextV2:
    file_path: str

    symbols: List[Any] = field(default_factory=list)
    relationships: List[Any] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)
