# pipeline_v2/core/identity/resolution_workflow_engine_v2.py

from collections import defaultdict

from pipeline_v2.core.identity.resolution_workflow_v2 import (
    ResolutionEventV2,
)


class ResolutionWorkflowEngineV2:
    """
    Registro auditável das transições de resolução.

    Responsabilidades:
    - armazenar eventos emitidos;
    - recuperar histórico completo;
    - recuperar último evento;
    - permitir replay determinístico.

    NÃO:
    - resolve identidades;
    - mantém estado atual;
    - altera GraphCore;
    - executa reconciliação.
    """

    def __init__(self):
        self.transitions: dict[str, list[ResolutionEventV2]] = defaultdict(list)

    # =====================================================
    # EVENT REGISTRATION
    # =====================================================

    def emit(self, event: ResolutionEventV2) -> ResolutionEventV2:
        """
        Registra um evento imutável.

        Retorna o próprio evento para facilitar encadeamento.
        """

        self.transitions[event.source].append(event)

        return event

    # =====================================================
    # HISTORY
    # =====================================================

    def get_history(
        self,
        source: str,
    ) -> list[ResolutionEventV2]:

        return list(self.transitions.get(source, []))

    # =====================================================
    # LAST EVENT
    # =====================================================

    def get_last_event(
        self,
        source: str,
    ) -> ResolutionEventV2 | None:

        events = self.transitions.get(source)

        if not events:
            return None

        return events[-1]

    # =====================================================
    # REPLAY
    # =====================================================

    def replay(
        self,
        source: str,
    ):

        for event in self.transitions.get(source, []):
            yield event

    # =====================================================
    # FULL TRANSITION GRAPH
    # =====================================================

    def build_transition_graph(self) -> dict:

        return {
            source: [
                {
                    "event_type": event.event_type.value,
                    "target": event.target,
                    "evidence": list(event.evidence),
                    "confidence": event.confidence,
                    "context": dict(event.context),
                }
                for event in events
            ]
            for source, events in self.transitions.items()
        }

    # =====================================================
    # STATS
    # =====================================================

    def stats(self) -> dict:

        total_events = sum(len(events) for events in self.transitions.values())

        return {
            "tracked_sources": len(self.transitions),
            "total_events": total_events,
        }

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.transitions.clear()
