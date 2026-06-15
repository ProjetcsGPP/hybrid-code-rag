# pipeline_v2/core/identity/resolution_workflow_v2.py

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ResolutionEventTypeV2(str, Enum):
    """
    Eventos auditáveis do ciclo de vida da identidade.

    Esses eventos NÃO representam o resultado da resolução.
    O resultado é expresso por ResolutionResultV2.
    """

    CREATED = "CREATED"

    RESOLVED = "RESOLVED"

    PENDING_RESOLUTION = "PENDING_RESOLUTION"

    FAILED_RESOLUTION = "FAILED_RESOLUTION"

    PROMOTION = "PROMOTION"

    RECONCILIATION = "RECONCILIATION"

    MERGE = "MERGE"

    CANONICALIZATION = "CANONICALIZATION"

    REJECTED = "REJECTED"


@dataclass(frozen=True)
class ResolutionEventV2:
    """
    Evento imutável utilizado exclusivamente
    para auditoria e reconstrução histórica.

    Não representa estado atual.

    Não é utilizado como retorno de resolve().

    O estado atual é obtido através de ResolutionResultV2.
    """

    event_type: ResolutionEventTypeV2

    source: str

    target: str | None = None

    evidence: list[str] = field(default_factory=list)

    confidence: float = 0.0

    context: dict[str, Any] = field(default_factory=dict)

    def is_success(self) -> bool:
        return self.event_type in (
            ResolutionEventTypeV2.RESOLVED,
            ResolutionEventTypeV2.PROMOTION,
            ResolutionEventTypeV2.RECONCILIATION,
            ResolutionEventTypeV2.MERGE,
            ResolutionEventTypeV2.CANONICALIZATION,
        )

    def is_failure(self) -> bool:
        return self.event_type in (
            ResolutionEventTypeV2.FAILED_RESOLUTION,
            ResolutionEventTypeV2.REJECTED,
        )
