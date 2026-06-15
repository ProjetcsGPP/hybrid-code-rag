# pipeline_v2/core/relationship/relationship_core.py

from .relationship_factory import RelationshipFactoryV2
from .relationship_resolver import RelationshipResolverV2

from pipeline_v2.core.state.semantic_context import SemanticContextV2
from pipeline_v2.core.state.assignment_resolver import AssignmentResolverV2

from pipeline_v2.core.resolution.symbol_resolution_engine_v2 import (
    SymbolResolutionEngineV2,
)

from pipeline_v2.core.identity.identity_mode import IdentityMode
from pipeline_v2.core.graph.graph_types import GraphNodeV2

from pipeline_v2.core.state.semantic_inference import (
    SemanticInferenceEngineV2,
)
from pipeline_v2.core.identity.resolution_workflow_engine_v2 import (
    ResolutionWorkflowEngineV2,
)

from pipeline_v2.core.semantic.semantic_authority import SemanticAuthority


from pipeline_v2.core.contract.contract_enforcer import ContractEnforcer


class RelationshipCoreV2:

    def __init__(
        self,
        symbol_core=None,
        graph_core=None,
        identity_registry=None,
    ):
        self.symbol_core = symbol_core
        self.graph_core = graph_core

        if identity_registry is None:
            raise ValueError("RelationshipCoreV2 requires shared identity_registry")

        self.identity_registry = identity_registry

        self.resolver = RelationshipResolverV2()
        self.workflow_engine = ResolutionWorkflowEngineV2()

        self.resolution_engine = SymbolResolutionEngineV2(
            symbol_core=symbol_core,
            graph_core=graph_core,
            identity_registry=self.identity_registry,
        )

        self.semantic_authority = SemanticAuthority()
        self.semantic_inference = SemanticInferenceEngineV2()

    # =========================================================
    # PUBLIC API
    # =========================================================

    def process_chunk(self, chunk, symbol_table):

        chunk = ContractEnforcer.enforce_chunk(chunk)

        relationships = []
        semantic_context = self._build_semantic_context(chunk)

        source = str(
            self.resolution_engine.resolve_source(
                chunk,
                symbol_table,
                self._chunk_id,
                self._chunk_metadata,
            )
        )

        if not source:
            return relationships

        resolved_source = self.identity_registry.resolve(source)

        if not resolved_source.is_resolved():
            self._ensure_identity_node(source, IdentityMode.INFERRED)
            resolved_source = self.identity_registry.resolve(source)

        if resolved_source.event:
            self.workflow_engine.emit(resolved_source.event)

        resolved_source_id = (
            resolved_source.require_identity()
            if resolved_source.is_resolved()
            else source
        )

        imports_hint = getattr(chunk, "imports_context", None)

        for raw_call in self._chunk_raw_calls(chunk):

            normalized_call = self.resolution_engine.normalize_call(raw_call)

            semantic_result = self.semantic_inference.resolve_call(
                raw_call=normalized_call["raw"],
                semantic_context=semantic_context,
            )

            state = None

            if "." in normalized_call["raw"]:
                owner = normalized_call["raw"].split(".", 1)[0]
                state = semantic_context.resolve_variable(owner)

            authority_decision = None

            if state:
                authority_decision = self.semantic_authority.decide(
                    state=state,
                    inference=semantic_result,
                )

            resolved = self.resolver.resolve_call(
                caller_symbol=resolved_source_id,
                raw_call=normalized_call["raw"],
                semantic_context=semantic_context,
            )

            if semantic_result:
                resolved.semantic = resolved.semantic.merge_inference(semantic_result)

            semantic_data = resolved.semantic

            # =========================================================
            # TARGET RESOLUTION (SEM fallback chain SEM CRIAÇÃO DE STRING)
            # =========================================================

            target = self.resolution_engine.resolve_semantic_target(
                semantic_data,
                symbol_table,
            )

            if not target:
                target = self.resolution_engine.resolve_target(
                    normalized_call["raw"],
                    symbol_table,
                )

            if not target:
                target = self._resolve_from_imports(
                    normalized_call["raw"],
                    imports_hint,
                )

            # ❌ REGRA NOVA: sem fallback textual, sem "external::", sem "unresolved::"
            if not target:
                continue

            resolved_target = self.identity_registry.resolve(str(target))

            if not resolved_target.is_resolved():
                self._ensure_identity_node(str(target), IdentityMode.INFERRED)
                resolved_target = self.identity_registry.resolve(str(target))

            resolved_target_id = (
                resolved_target.require_identity()
                if resolved_target.is_resolved()
                else str(target)
            )

            # proteção final: se ainda não tem identidade real → skip
            if not resolved_target_id:
                continue

            self._ensure_identity_node(resolved_source_id, IdentityMode.INFERRED)
            self._ensure_identity_node(resolved_target_id, IdentityMode.INFERRED)

            rel = RelationshipFactoryV2.create(
                source=str(resolved_source_id),
                target=str(resolved_target_id),
                type=resolved.relationship_type,
                dispatch=resolved.dispatch,
                raw_call=normalized_call["raw"],
                layer=resolved.layer,
                status="RESOLVED",
                confidence=resolved.confidence,
                provenance=(
                    authority_decision.provenance
                    if authority_decision
                    else semantic_data.provenance if semantic_data else "UNKNOWN"
                ),
                framework_hint=semantic_data.framework_hint if semantic_data else "",
                semantic_owner=(
                    authority_decision.model
                    if authority_decision
                    else semantic_data.resolved_owner if semantic_data else ""
                ),
                metadata=self._build_metadata(chunk, resolved),
            )

            relationships.append(rel)

        return relationships

    # =========================================================
    # METADATA
    # =========================================================

    def _build_metadata(self, chunk, inference):
        return {
            "chunk_id": self._chunk_id(chunk),
            "file": self._chunk_file(chunk),
            "semantic_resolution": bool(inference),
            "inference": inference.to_dict(),
        }

    # =========================================================
    # SEMANTIC CONTEXT
    # =========================================================

    def _build_semantic_context(self, chunk):

        context = SemanticContextV2()

        assignments = ContractEnforcer.enforce_assignments(chunk.assignments)

        for assignment in assignments:
            assignment = ContractEnforcer.enforce_assignment(assignment)

            state = AssignmentResolverV2().resolve(assignment)
            if state:
                context.set(state)

        return context

    # =========================================================
    # HELPERS
    # =========================================================

    def _chunk_metadata(self, chunk):
        return chunk.metadata

    def _chunk_raw_calls(self, chunk):
        return chunk.raw_calls

    def _chunk_id(self, chunk):
        return chunk.id

    def _chunk_file(self, chunk):
        return chunk.file

    def _resolve_from_imports(self, call: str, imports):
        if not imports:
            return None

        for imp in imports:
            local = imp.get("local_name", "")
            module = imp.get("module", "")

            if local and call.startswith(local):
                return f"{module}.{call}"

        return None

    # =========================================================
    # IDENTITY HANDLING
    # =========================================================

    def _ensure_identity_node(self, node_id: str, mode: IdentityMode):

        if self.identity_registry.exists(node_id):
            return

        if mode == IdentityMode.STRICT:
            return

        node_type = "inferred" if mode == IdentityMode.INFERRED else "external"

        self.identity_registry.register(
            GraphNodeV2(
                id=node_id,
                type=node_type,
                name=node_id,
                canonical=node_id,
                metadata={"mode": mode.value},
            )
        )
