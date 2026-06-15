# pipeline_v2/core/identity/resolution_result_v2.py

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from pipeline_v2.core.identity.resolution_workflow_v2 import (
    ResolutionEventV2,
)


class ResolutionStatusV2(str, Enum):
    """
    Estado final produzido pela autoridade de identidade.

    Representa o resultado da tentativa de resolução,
    independentemente da trilha de auditoria.
    """

    RESOLVED = "RESOLVED"

    PENDING = "PENDING"

    EXTERNAL = "EXTERNAL"

    FAILED = "FAILED"


@dataclass(frozen=True)
class ResolutionResultV2:
    """
    Contrato canônico de resolução.

    Este é o único retorno permitido para operações
    de resolução de identidade.

    Nunca utilizar:
    - str
    - None
    - ResolutionEventV2

    como retorno de APIs de resolução.
    """

    status: ResolutionStatusV2

    identity_id: str | None

    evidence: Tuple[str, ...] = ()

    confidence: float = 1.0

    event: ResolutionEventV2 | None = None

    # =====================================================
    # STATUS HELPERS
    # =====================================================

    def is_resolved(self) -> bool:
        return self.status == ResolutionStatusV2.RESOLVED

    def is_failed(self) -> bool:
        return self.status == ResolutionStatusV2.FAILED

    def is_pending(self) -> bool:
        return self.status == ResolutionStatusV2.PENDING

    def is_external(self) -> bool:
        return self.status == ResolutionStatusV2.EXTERNAL

    # =====================================================
    # ACCESS HELPERS
    # =====================================================

    def require_identity(self) -> str:
        """
        Retorna a identidade resolvida.

        Falha explicitamente caso não exista
        uma identidade consolidada.
        """

        if self.identity_id is None:
            raise ValueError("ResolutionResultV2 does not contain a resolved identity.")

        return self.identity_id

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "identity_id": self.identity_id,
            "evidence": list(self.evidence),
            "confidence": self.confidence,
            "event": (
                {
                    "event_type": self.event.event_type.value,
                    "source": self.event.source,
                    "target": self.event.target,
                    "context": self.event.context,
                    "confidence": getattr(
                        self.event,
                        "confidence",
                        1.0,
                    ),
                    "evidence": list(
                        getattr(
                            self.event,
                            "evidence",
                            (),
                        )
                    ),
                }
                if self.event
                else None
            ),
        }

    # =====================================================
    # FACTORY METHODS
    # =====================================================

    @classmethod
    def resolved(
        cls,
        identity_id: str,
        evidence: Tuple[str, ...] = (),
        confidence: float = 1.0,
        event: ResolutionEventV2 | None = None,
    ) -> "ResolutionResultV2":

        return cls(
            status=ResolutionStatusV2.RESOLVED,
            identity_id=identity_id,
            evidence=evidence,
            confidence=confidence,
            event=event,
        )

    @classmethod
    def failed(
        cls,
        evidence: Tuple[str, ...] = (),
        confidence: float = 0.0,
        event: ResolutionEventV2 | None = None,
    ) -> "ResolutionResultV2":

        return cls(
            status=ResolutionStatusV2.FAILED,
            identity_id=None,
            evidence=evidence,
            confidence=confidence,
            event=event,
        )

    @classmethod
    def pending(
        cls,
        evidence: Tuple[str, ...] = (),
        confidence: float = 0.0,
        event: ResolutionEventV2 | None = None,
    ) -> "ResolutionResultV2":

        return cls(
            status=ResolutionStatusV2.PENDING,
            identity_id=None,
            evidence=evidence,
            confidence=confidence,
            event=event,
        )

    @classmethod
    def external(
        cls,
        identity_id: str | None = None,
        evidence: Tuple[str, ...] = (),
        confidence: float = 1.0,
        event: ResolutionEventV2 | None = None,
    ) -> "ResolutionResultV2":

        return cls(
            status=ResolutionStatusV2.EXTERNAL,
            identity_id=identity_id,
            evidence=evidence,
            confidence=confidence,
            event=event,
        )
