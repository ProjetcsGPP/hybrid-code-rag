# pipeline_v2/core/relationships/relationship_index.py

from typing import Dict, List
from .relationship import Relationship


class RelationshipIndex:
    """
    Índice global de relações do grafo semântico.
    """

    def __init__(self):
        self.by_id: Dict[str, Relationship] = {}

        self.by_source: Dict[str, List[str]] = {}
        self.by_target: Dict[str, List[str]] = {}
        self.by_type: Dict[str, List[str]] = {}

    def add(self, rel: Relationship):
        self.by_id[rel.id] = rel

        self.by_source.setdefault(rel.source_id, []).append(rel.id)
        self.by_target.setdefault(rel.target_id, []).append(rel.id)
        self.by_type.setdefault(rel.relationship_type, []).append(rel.id)

    def get(self, rel_id: str) -> Relationship:
        return self.by_id[rel_id]

    def get_by_source(self, symbol_id: str) -> List[Relationship]:
        return [self.by_id[rid] for rid in self.by_source.get(symbol_id, [])]

    def get_by_target(self, symbol_id: str) -> List[Relationship]:
        return [self.by_id[rid] for rid in self.by_target.get(symbol_id, [])]

    def get_by_type(self, rel_type: str) -> List[Relationship]:
        return [self.by_id[rid] for rid in self.by_type.get(rel_type, [])]

    def all(self) -> List[Relationship]:
        return list(self.by_id.values())
