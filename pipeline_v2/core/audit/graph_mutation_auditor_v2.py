# pipeline_v2/core/audit/graph_mutation_auditor_v2.py

from dataclasses import dataclass
from typing import Optional, Dict, Any

from pipeline_v2.core.identity.identity_mode import IdentityMode


@dataclass
class MutationEvent:
    actor: str
    operation: str  # ADD_NODE | ADD_EDGE
    entity: Any
    source: Optional[str] = None
    target: Optional[str] = None
    trace: Optional[str] = None
    metadata: Dict[str, Any] = None


class GraphMutationAuditorV2:
    """
    Middleware de governança do grafo.

    Atua ANTES da persistência.
    """

    def __init__(self, identity_registry):
        self.identity_registry = identity_registry

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def audit(self, event: MutationEvent):
        """
        Decide se mutação pode ocorrer e como deve ser tratada.
        """

        if event.operation == "ADD_NODE":
            return self._audit_node(event)

        if event.operation == "ADD_EDGE":
            return self._audit_edge(event)

        return {"action": "ALLOW", "event": event}

    # =====================================================
    # NODE AUDIT
    # =====================================================

    def _audit_node(self, event: MutationEvent):

        node_id = getattr(event.entity, "id", None) or event.source

        if not node_id:
            return {"action": "BLOCK", "reason": "missing_node_id"}

        # já existe → ok
        if self.identity_registry.exists(node_id):
            return {
                "action": "ALLOW",
                "mode": IdentityMode.STRICT,
                "reason": "already_exists",
            }

        # heurística: external vs inferred
        if event.metadata and event.metadata.get("external"):
            mode = IdentityMode.EXTERNAL
        else:
            mode = IdentityMode.INFERRED

        return {
            "action": "ENRICH",
            "mode": mode,
            "entity_id": node_id,
        }

    # =====================================================
    # EDGE AUDIT
    # =====================================================

    def _audit_edge(self, event: MutationEvent):

        source = event.source
        target = event.target

        if not source or not target:
            return {"action": "BLOCK", "reason": "missing_endpoints"}

        # regra crítica: evita drift silencioso
        source_exists = self.identity_registry.exists(source)
        target_exists = self.identity_registry.exists(target)

        if not source_exists or not target_exists:
            return {
                "action": "ENRICH",
                "mode": IdentityMode.INFERRED,
                "missing": {
                    "source_missing": not source_exists,
                    "target_missing": not target_exists,
                },
            }

        return {"action": "ALLOW", "mode": IdentityMode.STRICT}
