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

        # ---------------------------------------------
        # by id
        # ---------------------------------------------

        if obj_id:
            self.by_id[obj_id] = obj

        # ---------------------------------------------
        # by name
        # ---------------------------------------------

        if name:

            if name not in self.by_name:
                self.by_name[name] = []

            self.by_name[name].append(obj)

        # ---------------------------------------------
        # by canonical
        # ---------------------------------------------

        if canonical:
            if canonical not in self.by_canonical:
                self.by_canonical[canonical] = obj

        return obj

    # =====================================================
    # RESOLVE ID
    # =====================================================

    def resolve_id(self, obj_id: str):

        return self.by_id.get(obj_id)

    # =====================================================
    # RESOLVE NAME
    # =====================================================

    def resolve_name(self, name: str):

        matches = self.by_name.get(name, [])

        if not matches:
            return None

        return matches[0].id

    def resolve_by_name(self, name: str):

        return self.by_name.get(name, [])

    def resolve_best_by_name(self, name: str):
        matches = self.by_name.get(name, [])
        return matches[0] if matches else None

    # =====================================================
    # RESOLVE CANONICAL
    # =====================================================

    def resolve_by_canonical(self, canonical: str):
        return self.by_canonical.get(canonical, None)

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
