# pipeline_v2/core/identity/resolution_state_v2.py


from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ResolutionStateTypeV2(str, Enum):
    RESOLVED = "RESOLVED"
    EXTERNAL = "EXTERNAL"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class ResolutionStateV2:
    """
    Estado canônico de resolução simbólica.

    Substitui completamente:
    - "external::"
    - "UNRESOLVED::"
    """

    state: ResolutionStateTypeV2
    value: str
    canonical: Optional[str] = None

    def is_resolved(self) -> bool:
        return self.state == ResolutionStateTypeV2.RESOLVED

    def is_external(self) -> bool:
        return self.state == ResolutionStateTypeV2.EXTERNAL

    def is_unresolved(self) -> bool:
        return self.state == ResolutionStateTypeV2.UNRESOLVED
