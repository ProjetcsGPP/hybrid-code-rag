# pipeline_v2/validation/contracts/metrics/identity_metrics.py

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class IdentityMetrics:

    registry_ids: int

    graph_nodes: int

    unused_registry_ids: int

    duplicate_ids: int

    duplicate_canonicals: int

    orphan_nodes: int

    unused_by_type: Dict[str, int] = field(default_factory=dict)

    orphan_by_type: Dict[str, int] = field(default_factory=dict)
