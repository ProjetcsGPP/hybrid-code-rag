# pipeline_v2/core/identity/deterministic_identity.py

import hashlib
from typing import Optional, List


class DeterministicIdentity:
    """
    Core deterministic identity generator.

    Regras:
    - SEM UUID
    - SEM estado interno
    - SEM dependência de graph
    - SEM side effects

    Objetivo:
    garantir que a mesma entrada SEMPRE gere o mesmo ID.
    """

    # =====================================================
    # SYMBOL ID
    # =====================================================

    @staticmethod
    def symbol_id(
        *,
        namespace: str,
        symbol_type: str,
        name: str,
        file_path: str,
        parent: Optional[str] = None,
        extras: Optional[List[str]] = None,
    ) -> str:
        """
        Deterministic ID for symbols.
        """

        raw = "|".join(
            [
                namespace or "",
                symbol_type or "",
                name or "",
                file_path or "",
                parent or "",
                *(extras or []),
            ]
        )

        return DeterministicIdentity._hash(raw)

    # =====================================================
    # RELATIONSHIP ID
    # =====================================================

    @staticmethod
    def relationship_id(
        *,
        source: str,
        target: str,
        relationship_type: str,
        dispatch: str = "DIRECT",
        layer: str = "STRUCTURAL",
        namespace: str = "",
        raw_call: str = "",
    ) -> str:
        """
        Deterministic ID for relationships.
        """

        raw = "|".join(
            [
                source or "",
                target or "",
                relationship_type or "",
                dispatch or "",
                layer or "",
                namespace or "",
                raw_call or "",
            ]
        )

        return DeterministicIdentity._hash(raw)

    # =====================================================
    # GENERIC HASH
    # =====================================================

    @staticmethod
    def _hash(value: str) -> str:
        """
        Stable hash function for all identities.
        """

        return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]

    # =====================================================
    # NORMALIZATION (LIGHTWEIGHT)
    # =====================================================

    @staticmethod
    def normalize(value: str) -> str:
        """
        Normalization used before hashing.
        """

        if not value:
            return ""

        return value.strip().lower()
