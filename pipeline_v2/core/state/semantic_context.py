# pipeline_v2/core/state/semantic_context.py

from typing import Dict, Optional

from pipeline_v2.core.contract.graph_contracts import AssignmentContractV2
from pipeline_v2.core.state.variable_state import VariableState


class SemanticContextV2:
    """
    Estado semântico transitório por chunk.

    Responsável por:
    - armazenar assignments inferidos
    - rastrear bindings locais
    - permitir propagation futura

    NÃO substitui:
    - graph runtime
    - symbol graph
    - legacy resolver

    Atua apenas como contexto semântico local.
    """

    def __init__(self):
        self.variables: Dict[str, VariableState] = {}

    # -------------------------
    # REGISTER VARIABLE
    # -------------------------
    def set(self, state: VariableState):

        self.variables[state.name] = state

    # -------------------------
    # GET VARIABLE
    # -------------------------
    def resolve_variable(self, name: str) -> Optional[VariableState]:

        return self.variables[name] if name in self.variables else None

    # -------------------------
    # ASSIGNMENT HYDRATION
    # -------------------------
    def update_from_assignments(self, assignments: list[AssignmentContractV2]):
        """
        Converte assignments AST já existentes
        em estado semântico transitório.

        NÃO cria inferência nova ainda.
        Apenas organiza estado local.
        """

        for a in assignments:

            var = a.variable

            if not var:
                continue

            state = VariableState(
                name=var,
                source=a.source,
                semantic_type=a.semantic_type,
                model=a.model,
                confidence=a.confidence,
                framework_hint=a.framework_hint,
                provenance="ASSIGNMENT_TRACKING",
                metadata={"raw_assignment": a},
            )

            self.set(state)

    # -------------------------
    # DEBUG
    # -------------------------
    def dump(self):

        return self.as_dict()

    def as_dict(self):
        return {k: v.to_dict() for k, v in self.variables.items()}
