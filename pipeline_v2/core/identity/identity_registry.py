# pipeline_v2/core/identity/identity_registry.py


class IdentityRegistryV2:
    """
    Single source of truth for:
    - symbols
    - nodes
    - edges
    - canonical identities
    """

    def __init__(self):
        self.by_id = {}
        self.by_name = {}
        self.by_canonical = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(self, obj):
        obj_id = getattr(obj, "id", None)
        name = getattr(obj, "name", None)
        canonical = getattr(obj, "canonical", None) or getattr(obj, "symbol_path", None)

        # -------------------------
        # ID INDEX (STRICT)
        # -------------------------
        if obj_id:
            self.by_id[obj_id] = obj

        # -------------------------
        # NAME INDEX (MULTI)
        # -------------------------
        if name:
            self.by_name.setdefault(name, [])
            self.by_name[name].append(obj)

        # -------------------------
        # CANONICAL INDEX (SAFE MODE)
        # -------------------------
        if canonical:
            if canonical in self.by_canonical:
                # 🔥 DETECTA COLISÃO EXPLICITA
                existing = self.by_canonical[canonical]
                if existing.id != obj_id:
                    raise ValueError(
                        f"Canonical collision detected: {canonical} "
                        f"({existing.id} vs {obj_id})"
                    )

            self.by_canonical[canonical] = obj

        return obj

    # =====================================================
    # RESOLUTION (SINGLE ENTRY POINT)
    # =====================================================

    def resolve(self, ref: str):
        """
        Unified identity resolution strategy:
        1. direct ID
        2. name match
        3. canonical match
        4. external fallback
        """

        if ref is None:
            return f"pending::{ref}"

        # 1. direct ID
        if ref in self.by_id:
            return ref

        # 2. name resolution (best match)
        matches = self.by_name.get(ref, [])
        if matches:
            return matches[0].id

        # 3. canonical resolution
        obj = self.by_canonical.get(ref)
        if obj:
            return obj.id

        # 4. fallback external reference
        return f"external::{ref}"

    # =====================================================
    # LOOKUPS
    # =====================================================

    def resolve_id(self, obj_id: str):
        return self.by_id.get(obj_id)

    def resolve_by_name(self, name: str):
        return self.by_name.get(name, [])

    def resolve_best_by_name(self, name: str):
        matches = self.by_name.get(name, [])
        return matches[0] if matches else None

    def resolve_by_canonical(self, canonical: str):
        obj = self.by_canonical.get(canonical)
        return obj.id if obj else None

    def get_all(self):
        return list(self.by_id.values())

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(self, obj_id: str):
        return obj_id in self.by_id

    # =====================================================
    # STATS
    # =====================================================

    def stats(self):
        return {
            "ids": len(self.by_id),
            "names": len(self.by_name),
            "canonicals": len(self.by_canonical),
        }

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):
        self.by_id.clear()
        self.by_name.clear()
        self.by_canonical.clear()
