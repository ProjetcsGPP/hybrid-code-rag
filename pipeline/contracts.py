from typing import TypedDict, List, Optional


class ChunkMeta(TypedDict, total=False):
    type: str
    name: str
    file: str
    chunk_id: str

    semantic_type: str
    semantic_top_concept: str
    semantic_confidence: float
    semantic_candidates: List[str]

    importance_score: float

    calls: List[str]


class ChunkResult(TypedDict):
    doc: str
    meta: ChunkMeta

    vector_score: float
    semantic_score: float
    structural_score: float

    importance_score: float
    intent_score: float

    final_score: float


class Symbol:
    def __init__(
        self,
        symbol_id: str,
        symbol_path: str,
        name: str,
        symbol_type: str,
        module_name: str,
        file_path: str,
        parent_symbol_id: Optional[str],
        semantic_type: str,
        start_line: int,
        end_line: int,
        calls: Optional[List[str]] = None,
    ):
        self.symbol_id = symbol_id
        self.symbol_path = symbol_path
        self.name = name
        self.symbol_type = symbol_type
        self.module_name = module_name
        self.file_path = file_path
        self.parent_symbol_id = parent_symbol_id
        self.semantic_type = semantic_type
        self.start_line = start_line
        self.end_line = end_line

        self.calls = calls or []

    def __repr__(self):
        return (
            f"Symbol("
            f"id={self.symbol_id}, "
            f"name={self.name}, "
            f"type={self.symbol_type}, "
            f"file={self.file_path}"
            f")"
        )


class Relationship:
    def __init__(
        self,
        relationship_id: str,
        source_symbol_id: str,
        target_symbol_id: str,
        relationship_type: str,
        confidence: float = 1.0,
    ):
        self.relationship_id = relationship_id
        self.source_symbol_id = source_symbol_id
        self.target_symbol_id = target_symbol_id
        self.relationship_type = relationship_type
        self.confidence = confidence
        
    def __repr__(self):
        return (
            f"Relationship("
            f"id={self.relationship_id}, "
            f"type={self.relationship_type}, "
            f"source={self.source_symbol_id}, "
            f"target={self.target_symbol_id}, "
            f"conf={self.confidence}"
            f")"
        )