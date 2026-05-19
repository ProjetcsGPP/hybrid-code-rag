from pipeline.structure.enums.edge_layer import EdgeLayer
from pipeline.structure.enums.resolution_status import ResolutionStatus
from pipeline.structure.enums.provenance_type import ProvenanceType
from pipeline.structure.enums.dispatch_type import DispatchType
from pipeline.structure.enums.resolver_stage import ResolverStage


class RelationshipSemanticMapper:
    """
    Camada TEMPORÁRIA de compatibilidade.

    Objetivo:
    - traduzir edge_types legados
    - enriquecer Relationship semanticamente
    - NÃO substituir edge_type ainda
    - NÃO alterar heurísticas existentes
    """

    @staticmethod
    def enrich(
        relationship,
        *,
        call_type: str | None = None,
        resolved: bool = True,
        framework_hint: str | None = None,
    ):

        relationship.relationship_type = (
            RelationshipSemanticMapper._normalize_relationship_type(
                relationship.relationship_type,
                call_type=call_type,
                resolved=resolved,
            )
        )

        relationship.layer = RelationshipSemanticMapper._map_layer(
            relationship.relationship_type,
            resolved,
        )

        relationship.resolution_status = (
            RelationshipSemanticMapper._map_resolution_status(
                relationship.relationship_type,
                resolved,
            )
        )

        relationship.provenance = RelationshipSemanticMapper._map_provenance(
            relationship.relationship_type,
        )

        relationship.dispatch_type = RelationshipSemanticMapper._map_dispatch_type(
            relationship.relationship_type,
            call_type,
        )

        relationship.framework_hint = framework_hint

        relationship.resolver_stage = RelationshipSemanticMapper._map_resolver_stage(
            relationship.relationship_type,
        )

        return relationship

    # ---------------------------------------------------------
    # LAYER
    # ---------------------------------------------------------

    @staticmethod
    def _map_layer(
        relationship_type: str,
        resolved: bool,
    ):

        if relationship_type == "BELONGS_TO":
            return EdgeLayer.STRUCTURAL.value

        if relationship_type.startswith("CALLS::"):

            if relationship_type in {
                "CALLS::UNRESOLVED",
                "CALLS::RUNTIME",
            }:
                return EdgeLayer.RUNTIME_APPROXIMATION.value

            return EdgeLayer.SEMANTIC_RESOLVED.value

        return EdgeLayer.STRUCTURAL.value

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    @staticmethod
    def _map_resolution_status(
        relationship_type: str,
        resolved: bool,
    ):

        if relationship_type == "CALLS::RUNTIME":
            return ResolutionStatus.RUNTIME_APPROXIMATION.value

        if relationship_type == "CALLS::UNRESOLVED":
            return ResolutionStatus.UNRESOLVABLE.value

        return ResolutionStatus.RESOLVED.value

    # ---------------------------------------------------------
    # PROVENANCE
    # ---------------------------------------------------------
    @staticmethod
    def _map_provenance(
        relationship_type: str,
    ):

        if relationship_type == "BELONGS_TO":
            return ProvenanceType.AST_DIRECT.value

        if relationship_type == "CALLS::EXTERNAL":
            return ProvenanceType.IMPORT_RESOLUTION.value

        if relationship_type.startswith("CALLS::"):
            return ProvenanceType.DYNAMIC_DISPATCH.value

        return ProvenanceType.AST_DIRECT.value

    # ---------------------------------------------------------
    # DISPATCH
    # ---------------------------------------------------------

    @staticmethod
    def _map_dispatch_type(
        relationship_type: str,
        call_type: str | None,
    ):

        if call_type == "self_method":
            return DispatchType.SELF.value

        if call_type == "super_method":
            return DispatchType.SUPER.value

        if relationship_type.startswith("CALLS::RUNTIME"):
            return DispatchType.DYNAMIC.value

        return DispatchType.DIRECT.value

    # ---------------------------------------------------------
    # RESOLVER STAGE
    # ---------------------------------------------------------

    @staticmethod
    def _map_resolver_stage(
        relationship_type: str,
    ):

        if relationship_type == "BELONGS_TO":
            return ResolverStage.AST_PASS.value

        if relationship_type.startswith("CALLS::"):
            return ResolverStage.SEMANTIC_PASS.value

        return ResolverStage.POST_PROCESS_PASS.value

    # ---------------------------------------------------------
    # NORMALIZATION
    # ---------------------------------------------------------

    @staticmethod
    def _normalize_relationship_type(
        relationship_type: str,
        *,
        call_type: str | None,
        resolved: bool,
    ):

        if relationship_type == "BELONGS_TO":
            return relationship_type

        if relationship_type.startswith("CALLS::"):
            return relationship_type

        if relationship_type in {
            "CALLS_INTERNAL",
            "CALLS_FUNCTION",
        }:

            if call_type == "super_method":
                return "CALLS::SUPER"

            if call_type == "self_method":

                if resolved:
                    return "CALLS::INHERITED"

                return "CALLS::RUNTIME"

            if resolved:
                return "CALLS::LOCAL"

            return "CALLS::UNRESOLVED"

        return relationship_type
