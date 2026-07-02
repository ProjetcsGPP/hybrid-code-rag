# pipeline_v2/validation/contracts/validation_result.py

# Este será o contrato central da observabilidade.


from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ValidationResult:

    summary: Dict[str, Any] = field(default_factory=dict)

    metrics: Dict[str, Any] = field(default_factory=dict)

    audits: Dict[str, Any] = field(default_factory=dict)

    warnings: List[str] = field(default_factory=list)

    errors: List[str] = field(default_factory=list)

    observations: List[str] = field(default_factory=list)
