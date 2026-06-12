# pipeline_v2/core/identity/identity_service_v2.py

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

    def exists(self, obj_id):
        return self.registry.exists(obj_id)

    # =====================================================
    # MAIN RESOLVE API
    # =====================================================

    def resolve(self, ref):
        return self.registry.resolve(ref)
