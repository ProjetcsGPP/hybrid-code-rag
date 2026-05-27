# pipeline_v2/core/identity/identity_strategy.py

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class IdentityStrategy:
    """
    Defines rules for deterministic identity generation.

    This layer exists so that identity rules can evolve
    without breaking core hashing logic.
    """

    namespace: str = "default"

    include_file_path: bool = True
    include_parent: bool = True
    include_raw_call: bool = True

    version: str = "v1"

    # =====================================================
    # SYMBOL STRATEGY BUILDER
    # =====================================================

    def build_symbol_context(
        self,
        *,
        symbol_type: str,
        name: str,
        file_path: str,
        parent: Optional[str] = None,
    ) -> dict:
        """
        Standardized symbol identity context.
        """

        return {
            "namespace": self.namespace,
            "symbol_type": symbol_type,
            "name": name,
            "file_path": file_path if self.include_file_path else "",
            "parent": parent if self.include_parent else "",
        }

    # =====================================================
    # RELATIONSHIP STRATEGY BUILDER
    # =====================================================

    def build_relationship_context(
        self,
        *,
        source: str,
        target: str,
        relationship_type: str,
        dispatch: str = "DIRECT",
        layer: str = "STRUCTURAL",
        raw_call: str = "",
    ) -> dict:
        """
        Standardized relationship identity context.
        """

        return {
            "namespace": self.namespace,
            "source": source,
            "target": target,
            "relationship_type": relationship_type,
            "dispatch": dispatch,
            "layer": layer,
            "raw_call": raw_call if self.include_raw_call else "",
        }

    # =====================================================
    # FUTURE HOOK (VERSIONING SUPPORT)
    # =====================================================

    def evolve(self, version: str) -> "IdentityStrategy":
        """
        Creates new strategy version without breaking old graphs.
        """

        return IdentityStrategy(
            namespace=self.namespace,
            include_file_path=self.include_file_path,
            include_parent=self.include_parent,
            include_raw_call=self.include_raw_call,
            version=version,
        )
