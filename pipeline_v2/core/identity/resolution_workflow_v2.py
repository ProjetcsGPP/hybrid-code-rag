# pipeline_v2/core/identity/resolution_workflow_v2.py

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ResolutionEventTypeV2(str, Enum):
    """
    Eventos que dirigem a evolução da resolução.
    """

    CREATED = "CREATED"
    RESOLVED = "RESOLVED"
    PROMOTED_TO_EXTERNAL = "PROMOTED_TO_EXTERNAL"
    FAILED_RESOLUTION = "FAILED_RESOLUTION"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class ResolutionEventV2:
    """
    Evento imutável de transição de estado.
    Substitui ResolutionStateV2 como unidade principal.
    """

    event_type: ResolutionEventTypeV2
    source: str
    target: Optional[str]
    context: Optional[dict] = None

    def is_success(self) -> bool:
        return self.event_type == ResolutionEventTypeV2.RESOLVED

    def is_failure(self) -> bool:
        return self.event_type in (
            ResolutionEventTypeV2.FAILED_RESOLUTION,
            ResolutionEventTypeV2.REJECTED,
        )
