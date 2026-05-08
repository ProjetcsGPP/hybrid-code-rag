from typing import TypedDict, List


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


class ChunkResult(TypedDict):
    doc: str
    meta: ChunkMeta

    vector_score: float
    semantic_score: float
    structural_score: float

    importance_score: float
    intent_score: float

    final_score: float