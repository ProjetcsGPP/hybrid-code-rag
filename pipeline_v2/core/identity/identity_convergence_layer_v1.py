# pipeline_v2/core/identity/identity_convergence_layer_v1.py

from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2


class IdentityConvergenceLayerV1:
    """
    Garante identidade canônica única entre todas as camadas:
    SymbolV2, GraphNodeV2, RelationshipV2
    """

    def __init__(self, identity_registry: IdentityRegistryV2):
        self.registry = identity_registry

    # ------------------------------------------
    # SINGLE ENTRY POINT
    # ------------------------------------------
    def resolve(self, ref):

        if ref is None:
            return f"pending::{ref}"

        # 1. já é id direto
        if self.registry.exists(ref):
            return ref

        # 2. resolve por nome
        by_name = self.registry.resolve_best_by_name(ref)
        if by_name:
            return by_name.id

        # 3. resolve por canonical
        by_canonical = self.registry.resolve_by_canonical(ref)
        if by_canonical:
            return by_canonical.id

        # 4. fallback (external dependency)
        return f"external::{ref}"

    # =====================================================
    # STR RESOLUTION
    # =====================================================

    def _resolve_str(self, value: str):

        if self.identity_registry and value in self.identity_registry.by_id:
            return value

        # fallback: tenta canonical lookup
        resolved = self._resolve_canonical(value)
        if resolved:
            return resolved

        return value

    # =====================================================
    # CANONICAL RESOLUTION
    # =====================================================

    def _resolve_canonical(self, canonical: str):

        if not self.identity_registry:
            return canonical

        obj = self.identity_registry.resolve_by_canonical(canonical)

        if obj:
            return getattr(obj, "id", canonical)

        return canonical
