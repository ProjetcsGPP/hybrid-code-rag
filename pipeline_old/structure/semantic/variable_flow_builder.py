# pipeline/structure/semantic/variable_flow_builder.py

from pipeline.structure.models.variable_binding import (
    VariableBinding,
)


class VariableFlowBuilder:

    def build_registry(self, symbol):

        registry = {}

        for assignment in symbol.assignments:

            # -------------------------------------------------
            # Recupera binding anterior
            # -------------------------------------------------

            existing = registry.get(assignment["variable"])

            semantic_type = assignment["semantic_type"]

            model_name = assignment.get("model")

            # -------------------------------------------------
            # Preserva inferência anterior mais forte
            # -------------------------------------------------

            if existing:

                if existing.semantic_type and existing.semantic_type != "unknown":
                    semantic_type = existing.semantic_type

                if existing.model_name and not model_name:
                    model_name = existing.model_name

            # -------------------------------------------------
            # Cria novo binding
            # -------------------------------------------------

            binding = VariableBinding(
                variable_name=assignment["variable"],
                semantic_type=semantic_type,
                inferred_from=assignment["source"],
                model_name=model_name,
                confidence=0.9,
            )

            registry[binding.variable_name] = binding

        return registry
