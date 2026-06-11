# pipeline_v2/core/semantic/canonical_semantic_normalizer_v2.py


class CanonicalSemanticNormalizerV2:
    """
    Elimina duplicação semântica entre:
    - SELF
    - SUPER
    - ORM / framework calls

    Gera representação única e canônica.
    """

    def normalize(self, edges):
        if not isinstance(edges, list):
            return []

        normalized = []

        for rel in edges:
            if not isinstance(rel, dict):
                continue
            normalized.append(self._normalize(rel))

        return normalized

    # -----------------------------------------
    # CORE LOGIC
    # -----------------------------------------

    def _normalize(self, rel: dict) -> dict:

        if not isinstance(rel, dict):
            raise TypeError(f"Expected dict relationship, got {type(rel)}")

        rel_type = rel.get("type")

        if rel_type in ["CALLS", "CALLS::SELF"]:
            return self._normalize_self(rel)

        if rel_type in ["CALLS::SUPER"]:
            return self._normalize_super(rel)

        if self._is_orm_call(rel):
            return self._normalize_orm(rel)

        return rel

    # -----------------------------------------
    # SELF NORMALIZATION
    # -----------------------------------------

    def _normalize_self(self, rel: dict) -> dict:

        rel["canonical_type"] = "CALLS_SELF"
        rel["semantic_role"] = "instance_method_call"
        rel["dispatch_mode"] = "SELF"

        return rel

    # -----------------------------------------
    # SUPER NORMALIZATION
    # -----------------------------------------

    def _normalize_super(self, rel: dict) -> dict:

        rel["canonical_type"] = "CALLS_SUPER"
        rel["semantic_role"] = "inheritance_chain_call"
        rel["dispatch_mode"] = "SUPER"

        return rel

    # -----------------------------------------
    # ORM NORMALIZATION
    # -----------------------------------------

    def _normalize_orm(self, rel: dict) -> dict:

        rel["canonical_type"] = "CALLS_ORM"
        rel["semantic_role"] = "framework_dispatch"
        rel["dispatch_mode"] = "FRAMEWORK"

        return rel

    # -----------------------------------------
    # DETECTOR
    # -----------------------------------------

    def _is_orm_call(self, rel: dict) -> bool:

        target = rel.get("target", "")

        orm_signatures = [
            "objects.",
            ".filter",
            ".get",
            ".exclude",
            ".save",
            ".update",
            "QuerySet",
        ]

        return any(sig in target for sig in orm_signatures)
