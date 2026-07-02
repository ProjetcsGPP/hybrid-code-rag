# pipeline_v2/validation/contracts/validation_context.py

# Este contrato representa tudo o que o pipeline produziu e que será observado.

from dataclasses import dataclass
from pathlib import Path
from typing import Any, List


@dataclass(frozen=True)
class ValidationContext:

    project_root: Path

    runtime: Any

    snapshot: Any  # ✅ NOVO CANAL OFICIAL

    identity_registry: Any

    graph_core: Any

    chunks: List[Any]

    symbols: List[Any]

    relationships: List[Any]

    execution_time: float = 0.0
