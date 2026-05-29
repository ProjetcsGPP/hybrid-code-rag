# pipeline_v2/core/identity/identity_service_v2.py

from typing import Optional
from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2


class IdentityServiceV2:
    """
    SINGLE SOURCE OF TRUTH for identity resolution.

    Replaces:
    - Convergence Layer logic duplication
    - scattered resolve() logic
    """

    def __init__(self, registry: IdentityRegistryV2):
        self.registry = registry

    # =====================================================
    # MAIN RESOLVE API
    # =====================================================

    def resolve(self, ref: Optional[str]) -> str:
        """
        Deterministic identity resolution pipeline:

        1. direct id
        2. name
        3. canonical
        4. external fallback
        """

        if ref is None:
            return "pending::null"

        # 1. direct ID
        if self.registry.exists(ref):
            return ref

        # 2. name resolution
        best = self.registry.resolve_best_by_name(ref)
        if best:
            return best.id

        # 3. canonical resolution
        canonical_id = self.registry.resolve_by_canonical(ref)
        if canonical_id:
            return canonical_id

        # 4. fallback external
        return f"external::{ref}"
