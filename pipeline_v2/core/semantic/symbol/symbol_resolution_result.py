# pipeline_v2/core/semantic/symbol/symbol_resolution_result.py

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class SymbolResolutionResult:

    resolved_owner: Optional[str] = None

    resolved_target: Optional[str] = None

    semantic_type: Optional[str] = None

    framework_hint: Optional[str] = None

    confidence: float = 0.0

    provenance: str = "UNKNOWN"

    normalized_call: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)
