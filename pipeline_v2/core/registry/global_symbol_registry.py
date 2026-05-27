# pipeline_v2/core/registry/global_symbol_registry.py

from typing import Dict, Optional, List
from collections import defaultdict


class GlobalSymbolRegistry:
    """
    Global Symbol Registry (GSR)

    SINGLE SOURCE OF TRUTH for all symbol identities.

    Responsável por:
    - canonical symbol lookup
    - alias resolution
    - deduplication base
    - namespace isolation
    """

    def __init__(self):
        # canonical_id -> symbol
        self._symbols: Dict[str, dict] = {}

        # name -> canonical_ids
        self._name_index: Dict[str, List[str]] = defaultdict(list)

        # namespace -> canonical_ids
        self._namespace_index: Dict[str, List[str]] = defaultdict(list)

        # alias -> canonical_id
        self._alias_map: Dict[str, str] = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(self, symbol: dict) -> str:
        """
        Registers a symbol in global registry.

        symbol MUST contain:
        - symbol_id (canonical deterministic id)
        - name
        - module_name or namespace
        """

        canonical_id = symbol["symbol_id"]

        # -------------------------------------------------
        # 1. EXISTING SYMBOL CHECK
        # -------------------------------------------------

        if canonical_id in self._symbols:
            return canonical_id

        # -------------------------------------------------
        # 2. STORE SYMBOL
        # -------------------------------------------------

        self._symbols[canonical_id] = symbol

        # -------------------------------------------------
        # 3. NAME INDEX
        # -------------------------------------------------

        name = symbol.get("name")
        if name:
            self._name_index[name].append(canonical_id)

        # -------------------------------------------------
        # 4. NAMESPACE INDEX
        # -------------------------------------------------

        namespace = self._extract_namespace(symbol)
        if namespace:
            self._namespace_index[namespace].append(canonical_id)

        # -------------------------------------------------
        # 5. ALIAS INIT (future-ready)
        # -------------------------------------------------

        canonical_name = symbol.get("canonical_name")
        if canonical_name:
            self._alias_map[canonical_name] = canonical_id

        return canonical_id

    # =====================================================
    # LOOKUP BY ID
    # =====================================================

    def get(self, canonical_id: str) -> Optional[dict]:
        return self._symbols.get(canonical_id)

    # =====================================================
    # LOOKUP BY NAME
    # =====================================================

    def find_by_name(self, name: str) -> List[dict]:
        ids = self._name_index.get(name, [])
        return [self._symbols[i] for i in ids if i in self._symbols]

    # =====================================================
    # LOOKUP BY NAMESPACE
    # =====================================================

    def find_by_namespace(self, namespace: str) -> List[dict]:
        ids = self._namespace_index.get(namespace, [])
        return [self._symbols[i] for i in ids if i in self._symbols]

    # =====================================================
    # RESOLVE CANONICAL
    # =====================================================

    def resolve(self, identifier: str) -> Optional[dict]:
        """
        Resolve:
        - canonical id
        - alias
        - name fallback
        """

        # 1. direct canonical
        if identifier in self._symbols:
            return self._symbols[identifier]

        # 2. alias
        alias_target = self._alias_map.get(identifier)
        if alias_target:
            return self._symbols.get(alias_target)

        # 3. name fallback (first match)
        candidates = self._name_index.get(identifier)
        if candidates:
            return self._symbols.get(candidates[0])

        return None

    # =====================================================
    # RECONCILIATION HOOK (FUTURE NORMALIZER)
    # =====================================================

    def reconcile(self, canonical_id: str, new_symbol: dict):
        """
        Future hook for GraphNormalizerV2.

        Will merge duplicates / update metadata.
        """

        existing = self._symbols.get(canonical_id)

        if not existing:
            return self.register(new_symbol)

        # merge metadata safely
        existing_meta = existing.get("metadata", {})
        new_meta = new_symbol.get("metadata", {})

        existing_meta.update(new_meta)
        existing["metadata"] = existing_meta

        return canonical_id

    # =====================================================
    # INTERNAL
    # =====================================================

    def _extract_namespace(self, symbol: dict) -> str:
        """
        Lightweight namespace inference.

        No semantic logic here — only structural grouping.
        """

        file_path = symbol.get("file_path", "")

        if not file_path:
            return "unknown"

        parts = file_path.replace("\\", "/").split("/")

        # heuristic: project root grouping
        if len(parts) > 2:
            return parts[-2]

        return parts[0]
