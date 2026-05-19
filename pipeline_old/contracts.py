# pipeline/contracts.py

from typing import TypedDict, List, Optional, Literal

EdgeType = Literal[
    "BELONGS_TO",
    "CALLS_INTERNAL",
    "INHERITS",
]


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
        canonical_name: str,
        name: str,
        symbol_type: str,
        module_name: str,
        file_path: str,
        parent_symbol_id: Optional[str],
        semantic_type: str,
        start_line: int,
        end_line: int,
        calls: Optional[List[str]] = None,
        imports: Optional[List[dict]] = None,
        bases: Optional[List[str]] = None,
        # -----------------------------------------
        # VARIABLE FLOW
        # -----------------------------------------
        assignments: Optional[List[dict]] = None,
    ):
        self.symbol_id = symbol_id
        self.symbol_path = symbol_path
        self.canonical_name = canonical_name
        self.name = name
        self.symbol_type = symbol_type
        self.module_name = module_name
        self.file_path = file_path
        self.parent_symbol_id = parent_symbol_id
        self.semantic_type = semantic_type
        self.start_line = start_line
        self.end_line = end_line

        self.calls = calls or []
        self.imports = imports or []
        self.bases = bases or []
        self.assignments = assignments or []

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
        # -----------------------------------------
        # SEMANTIC GRAPH STRATIFICATION
        # -----------------------------------------
        layer: str | None = None,
        resolution_status: str | None = None,
        provenance: str | None = None,
        dispatch_type: str | None = None,
        framework_hint: str | None = None,
        resolver_stage: str | None = None,
    ):

        # -----------------------------------------
        # LEGACY FIELDS
        # -----------------------------------------

        self.relationship_id = relationship_id

        self.source_symbol_id = source_symbol_id

        self.target_symbol_id = target_symbol_id

        self.relationship_type = relationship_type

        self.confidence = confidence

        # -----------------------------------------
        # SEMANTIC STRATIFICATION
        # -----------------------------------------

        self.layer = layer

        self.resolution_status = resolution_status

        self.provenance = provenance

        self.dispatch_type = dispatch_type

        self.framework_hint = framework_hint

        self.resolver_stage = resolver_stage

    def to_dict(self):

        return {
            "relationship_id": self.relationship_id,
            "source_symbol_id": self.source_symbol_id,
            "target_symbol_id": self.target_symbol_id,
            "relationship_type": self.relationship_type,
            "confidence": self.confidence,
            "layer": self.layer,
            "resolution_status": self.resolution_status,
            "provenance": self.provenance,
            "dispatch_type": self.dispatch_type,
            "framework_hint": self.framework_hint,
            "resolver_stage": self.resolver_stage,
        }

    def __repr__(self):

        return (
            "Relationship("
            f"id={self.relationship_id}, "
            f"type={self.relationship_type}, "
            f"source={self.source_symbol_id}, "
            f"target={self.target_symbol_id}, "
            f"conf={self.confidence}, "
            f"layer={self.layer}, "
            f"status={self.resolution_status}, "
            f"dispatch={self.dispatch_type}, "
            f"prov={self.provenance}, "
            f"stage={self.resolver_stage}"
            ")"
        )
