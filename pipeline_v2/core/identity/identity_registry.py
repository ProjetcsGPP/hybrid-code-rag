# pipeline_v2/core/identity/identity_registry.py

from pipeline_v2.core.identity.resolution_result_v2 import (
    ResolutionResultV2,
    ResolutionStatusV2,
)

from pipeline_v2.core.identity.resolution_workflow_v2 import (
    ResolutionEventV2,
    ResolutionEventTypeV2,
)


class IdentityRegistryV2:
    """
    Single Source of Truth para identidade.

    Responsável por:
    - registro;
    - resolução;
    - promoção;
    - reconciliação;
    - índices canônicos.

    Nenhuma outra camada deve implementar lógica de identidade.
    """

    def __init__(self):
        self.by_id = {}
        self.by_name = {}
        self.by_canonical = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(self, obj):

        obj_id = getattr(obj, "id", None)

        name = getattr(obj, "name", None)

        canonical = getattr(obj, "canonical", None) or getattr(obj, "symbol_path", None)

        # -------------------------
        # ID INDEX
        # -------------------------

        if obj_id:
            self.by_id[obj_id] = obj

        # -------------------------
        # NAME INDEX
        # -------------------------

        if name:

            if name not in self.by_name:
                self.by_name[name] = []

            self.by_name[name].append(obj)

        # -------------------------
        # CANONICAL INDEX
        # -------------------------

        if canonical:

            if canonical in self.by_canonical:

                existing = self.by_canonical[canonical]

                if existing.id != obj_id:
                    raise ValueError(
                        f"Canonical collision detected: "
                        f"{canonical} "
                        f"({existing.id} vs {obj_id})"
                    )

            self.by_canonical[canonical] = obj

        return obj

    # =====================================================
    # INTERNAL RESULT BUILDERS
    # =====================================================

    def _resolved_result(
        self,
        identity_id: str,
        evidence: tuple[str, ...],
        confidence: float,
    ) -> ResolutionResultV2:

        event = ResolutionEventV2(
            event_type=ResolutionEventTypeV2.RESOLVED,
            source=identity_id,
            target=identity_id,
            evidence=list(evidence),
            confidence=confidence,
        )

        return ResolutionResultV2(
            status=ResolutionStatusV2.RESOLVED,
            identity_id=identity_id,
            evidence=evidence,
            confidence=confidence,
            event=event,
        )

    def _failed_result(
        self,
        ref: str,
        reason: str,
    ) -> ResolutionResultV2:

        event = ResolutionEventV2(
            event_type=ResolutionEventTypeV2.FAILED_RESOLUTION,
            source=str(ref),
            target=None,
            context={
                "reason": reason,
            },
            confidence=0.0,
            evidence=[reason],
        )

        return ResolutionResultV2(
            status=ResolutionStatusV2.FAILED,
            identity_id=None,
            evidence=[reason],
            confidence=0.0,
            event=event,
        )

    def _pending_result(
        self,
        ref: str,
        reason: str = "pending",
    ) -> ResolutionResultV2:

        event = ResolutionEventV2(
            event_type=ResolutionEventTypeV2.PENDING_RESOLUTION,
            source=str(ref),
            target=None,
            context={
                "reason": reason,
            },
            confidence=0.0,
            evidence=[reason],
        )

        return ResolutionResultV2(
            status=ResolutionStatusV2.PENDING,
            identity_id=None,
            evidence=[reason],
            confidence=0.0,
            event=event,
        )

    def _external_result(
        self,
        ref: str,
        identity_id: str | None = None,
    ) -> ResolutionResultV2:

        event = ResolutionEventV2(
            event_type=ResolutionEventTypeV2.PROMOTION,
            source=str(ref),
            target=identity_id,
            evidence=["external"],
            confidence=1.0,
        )

        return ResolutionResultV2(
            status=ResolutionStatusV2.EXTERNAL,
            identity_id=identity_id,
            evidence=("external",),
            confidence=1.0,
            event=event,
        )

    # =====================================================
    # RESOLUTION
    # =====================================================

    def resolve(self, ref: str) -> ResolutionResultV2:
        """
        Único ponto de entrada para resolução.

        Nunca retorna:
        - str
        - ResolutionEventV2
        - None
        """

        if ref is None:
            return self._failed_result(
                ref="None",
                reason="null_ref",
            )

        # -------------------------------------------------
        # DIRECT ID
        # -------------------------------------------------

        if ref in self.by_id:

            return self._resolved_result(
                identity_id=ref,
                evidence=("direct_id",),
                confidence=1.0,
            )

        # -------------------------------------------------
        # NAME
        # -------------------------------------------------

        matches = self.by_name.get(ref, [])

        if matches:

            return self._resolved_result(
                identity_id=matches[0].id,
                evidence=("name_match",),
                confidence=0.90,
            )

        # -------------------------------------------------
        # CANONICAL
        # -------------------------------------------------

        obj = self.by_canonical.get(ref)

        if obj:

            return self._resolved_result(
                identity_id=obj.id,
                evidence=("canonical_match",),
                confidence=0.95,
            )

        # -------------------------------------------------
        # FAILURE
        # -------------------------------------------------

        return self._failed_result(
            ref=ref,
            reason="not_found",
        )

    # =====================================================
    # PROMOTION
    # =====================================================

    def promote(
        self,
        source: str,
        identity_id: str,
    ) -> ResolutionResultV2:
        """
        Reserva arquitetural para Closure/Reconciliation.
        """

        return self._external_result(
            ref=source,
            identity_id=identity_id,
        )

    # =====================================================
    # RECONCILIATION
    # =====================================================

    def reconcile(
        self,
        source: str,
        canonical_id: str,
    ) -> ResolutionResultV2:
        """
        Consolida uma identidade provisória
        em uma identidade canônica.
        """

        event = ResolutionEventV2(
            event_type=ResolutionEventTypeV2.RECONCILIATION,
            source=source,
            target=canonical_id,
            evidence=["reconciled"],
            confidence=1.0,
        )

        return ResolutionResultV2(
            status=ResolutionStatusV2.RESOLVED,
            identity_id=canonical_id,
            evidence=("reconciled",),
            confidence=1.0,
            event=event,
        )

    # =====================================================
    # LOOKUPS
    # =====================================================

    def resolve_id(self, obj_id: str):
        return self.by_id.get(obj_id)

    def resolve_by_name(self, name: str):
        return self.by_name.get(name, [])

    def resolve_best_by_name(self, name: str):

        matches = self.by_name.get(name, [])

        return matches[0] if matches else None

    def resolve_by_canonical(self, canonical: str):

        obj = self.by_canonical.get(canonical)

        return obj.id if obj else None

    def get_all(self):
        return list(self.by_id.values())

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(self, obj_id: str):
        return obj_id in self.by_id

    # =====================================================
    # STATS
    # =====================================================

    def stats(self):

        return {
            "ids": len(self.by_id),
            "names": len(self.by_name),
            "canonicals": len(self.by_canonical),
        }

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.by_id.clear()

        self.by_name.clear()

        self.by_canonical.clear()
