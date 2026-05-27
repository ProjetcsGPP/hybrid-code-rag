# pipeline_v2/core/state/semantic_context.py

from typing import Dict, Optional

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
    def get(self, name: str) -> Optional[VariableState]:

        return self.variables.get(name)

    # -------------------------
    # ASSIGNMENT HYDRATION
    # -------------------------
    def update_from_assignments(self, assignments: list):
        """
        Converte assignments AST já existentes
        em estado semântico transitório.

        NÃO cria inferência nova ainda.
        Apenas organiza estado local.
        """

        for a in assignments:

            var = a.get("variable")

            if not var:
                continue

            state = VariableState(
                name=var,
                source=a.get("source"),
                semantic_type=a.get("semantic_type", "unknown"),
                model=a.get("model"),
                confidence=a.get("confidence", 0.75),
                framework_hint=a.get("framework_hint"),
                provenance="ASSIGNMENT_TRACKING",
                metadata={"raw_assignment": a},
            )

            self.set(state)

    # -------------------------
    # DEBUG
    # -------------------------
    def dump(self):

        return {k: vars(v) for k, v in self.variables.items()}
