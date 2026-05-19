# pipeline_v2/core/symbol/symbol_factory.py

import uuid
from .symbol_models import SymbolV2
from .symbol_types import SymbolType


class SymbolFactoryV2:

    @staticmethod
    def create(
        name: str,
        type: SymbolType,
        file_path: str,
        parent: str = None,
        canonical: str = None,
        bases=None,
        metadata=None,
    ):

        symbol_id = f"{file_path}::{name}::{uuid.uuid4().hex[:8]}"

        return SymbolV2(
            id=symbol_id,
            name=name,
            type=type,
            file_path=file_path,
            canonical=canonical or f"{file_path}.{name}",
            parent=parent,
            bases=bases or [],
            metadata=metadata or {},
        )
