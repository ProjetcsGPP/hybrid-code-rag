# pipeline_v2/tests/test_identity_unified.py

from pipeline_v2.core.identity.identity_registry import IdentityRegistryV2
from pipeline_v2.core.identity.identity_service_v2 import IdentityServiceV2

from pipeline_v2.core.identity.resolution_workflow_v2 import (
    ResolutionEventTypeV2,
)
from pipeline_v2.core.identity.resolution_result_v2 import (
    ResolutionStatusV2,
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

    assert service.resolve("id_1").require_identity() == "id_1"
    assert service.resolve("alpha").require_identity() == "id_1"
    assert service.resolve("file.b").require_identity() == "id_2"

    result = service.resolve("unknown")

    assert result.status == ResolutionStatusV2.FAILED
    assert result.identity_id is None

    assert result.event is not None
    assert result.event.event_type == ResolutionEventTypeV2.FAILED_RESOLUTION

    assert result.event.source == "unknown"
    assert result.event.target is None

    print("✔ IDENTITY UNIFIED OK")
