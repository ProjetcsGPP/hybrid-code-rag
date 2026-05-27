# pipeline_v2/core/profiling/semantic_profile.py

from dataclasses import dataclass, field
from typing import List


@dataclass
class SemanticProfile:

    primary_language: str | None = None

    language_family: str | None = None

    primary_framework: str | None = None

    frameworks: List[str] = field(default_factory=list)

    variants: List[str] = field(default_factory=list)

    confidence: float = 0.0

    repository_type: str | None = None

    dominant_runtime: str | None = None

    evidence: List[str] = field(default_factory=list)
