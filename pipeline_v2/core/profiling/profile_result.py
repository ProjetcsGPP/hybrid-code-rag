# pipeline_v2/core/profiling/profile_result.py

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ProfileResult:

    language: str | None = None
    language_family: str | None = None

    framework: str | None = None
    frameworks: List[str] = field(default_factory=list)

    variant: str | None = None

    confidence: float = 0.0

    evidence: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)
