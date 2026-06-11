# pipeline_v2/core/identity/resolution_workflow_engine_v2.py

from collections import defaultdict
from .resolution_workflow_v2 import ResolutionEventV2


class ResolutionWorkflowEngineV2:
    """
    Mantém o grafo de transições de resolução.
    """

    def __init__(self):
        self.transitions = defaultdict(list)

    def emit(self, event: ResolutionEventV2):
        """
        Registra evento no grafo de transição.
        """
        self.transitions[event.source].append(event)

    def get_history(self, source: str):
        return self.transitions[source] if source in self.transitions else []

    def get_last_state(self, source: str):
        events = self.transitions[source] if source in self.transitions else []
        return events[-1] if events else None

    def build_transition_graph(self):
        graph = {}

        for source, events in self.transitions.items():
            graph[source] = [
                {
                    "event": e.event_type,
                    "target": e.target,
                    "context": e.context,
                }
                for e in events
            ]

        return graph
