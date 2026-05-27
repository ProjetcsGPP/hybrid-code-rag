# pipeline_v2/core/symbol/symbol_factory.py

from .symbol_models import SymbolV2
from .symbol_types import SymbolType

from pipeline_v2.core.identity.identity_strategy import IdentityStrategy


class SymbolFactoryV2:
    """
    Factory agora é puramente composicional.

    NÃO gera mais identidade.
    NÃO usa UUID.
    """

    @staticmethod
    def create(
        name: str,
        type: SymbolType,
        file_path: str,
        parent: str = None,
        canonical: str = None,
        bases=None,
        metadata=None,
        strategy: IdentityStrategy = IdentityStrategy(),
    ):
        """
        Criação determinística baseada em Identity Layer.
        """

        # -------------------------------------------------
        # 1. BUILD CONTEXT VIA STRATEGY
        # -------------------------------------------------

        context = strategy.build_symbol_context(
            symbol_type=type.value if hasattr(type, "value") else str(type),
            name=name,
            file_path=file_path,
            parent=parent,
        )

        # -------------------------------------------------
        # 2. CANONICAL IDENTITY
        # -------------------------------------------------

        canonical_name = canonical or f"{file_path}.{name}"

        symbol_id = canonical_name

        # -------------------------------------------------
        # 3. CANONICAL NAME (ESTÁVEL)
        # -------------------------------------------------

        canonical_name = canonical or f"{file_path}.{name}"

        # -------------------------------------------------
        # 4. BUILD SYMBOL
        # -------------------------------------------------

        return SymbolV2(
            id=symbol_id,
            name=name,
            type=type,
            file_path=file_path,
            canonical=canonical_name,
            parent=parent,
            bases=bases or [],
            metadata=metadata or {},
        )
