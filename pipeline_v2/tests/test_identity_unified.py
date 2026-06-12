# pipeline_v2/tests/test_identity_unified.py

from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2
from pipeline_v2.core.identity.identity_service_v2 import IdentityServiceV2

from pipeline_v2.core.identity.resolution_workflow_v2 import (
    ResolutionEventV2,
    ResolutionEventTypeV2,
)

registry = IdentityRegistryV2()
service = IdentityServiceV2(registry)


class Dummy:

    def __init__(self, id, name, canonical):
        self.id = id
        self.name = name
        self.canonical = canonical

    def test_identity_resolution():

        a = Dummy("id_1", "alpha", "file.a")
        b = Dummy("id_2", "beta", "file.b")

        registry.register(a)
        registry.register(b)

        assert service.resolve("id_1") == "id_1"
        assert service.resolve("alpha") == "id_1"
        assert service.resolve("file.b") == "id_2"

        result = service.resolve("unknown")

        assert isinstance(result, ResolutionEventV2)
        assert result.event_type == ResolutionEventTypeV2.FAILED_RESOLUTION
        assert result.source == "unknown"
        assert result.target is None

        print("✔ IDENTITY UNIFIED OK")
