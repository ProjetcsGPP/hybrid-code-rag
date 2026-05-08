from typing import Dict
from typing import List

import numpy as np


DEFAULT_CONCEPTS = [
    {
        "concept_name": "authorization",
        "parent_concept": None,
        "description": (
            "Authentication and authorization logic"
        ),
        "examples": [
            "jwt",
            "token",
            "permission",
            "role",
            "access control",
        ],
        "confidence": 1.0,
        "is_system": True,
    },
    {
        "concept_name": "validation",
        "parent_concept": None,
        "description": (
            "Input validation and data integrity"
        ),
        "examples": [
            "validate",
            "schema",
            "clean",
            "check",
        ],
        "confidence": 1.0,
        "is_system": True,
    },
    {
        "concept_name": "mutation",
        "parent_concept": None,
        "description": (
            "Data creation and update logic"
        ),
        "examples": [
            "create",
            "update",
            "delete",
            "save",
            "insert",
        ],
        "confidence": 1.0,
        "is_system": True,
    },
    {
        "concept_name": "query",
        "parent_concept": None,
        "description": (
            "Read and query operations"
        ),
        "examples": [
            "fetch",
            "get",
            "query",
            "list",
        ],
        "confidence": 1.0,
        "is_system": True,
    },
    {
        "concept_name": "business_logic",
        "parent_concept": None,
        "description": (
            "Core business rules and workflows"
        ),
        "examples": [
            "service",
            "workflow",
            "process",
            "rule",
        ],
        "confidence": 1.0,
        "is_system": True,
    },
]


class SemanticRegistry:

    def __init__(self, embedding_service):
        self.embedding_service = (
            embedding_service
        )

        self.concepts: Dict = {}

    def load_default_concepts(self):

        for concept in DEFAULT_CONCEPTS:
            self.register_concept(concept)

    def register_concept(self, concept):

        concept_text = " ".join([
            concept["concept_name"],
            concept["description"],
            " ".join(
                concept["examples"]
            ),
        ])

        embedding = (
            self.embedding_service
            .generate_concept_embedding(
                concept_text
            )
        )

        concept["embedding"] = embedding

        self.concepts[
            concept["concept_name"]
        ] = concept

    def cosine_similarity(
        self,
        a,
        b,
    ):
        a = np.array(a)
        b = np.array(b)

        denominator = (
            np.linalg.norm(a)
            * np.linalg.norm(b)
        )

        if denominator == 0:
            return 0.0

        return (
            np.dot(a, b) / denominator
        )

    def find_similar_concepts(
        self,
        chunk_embedding,
        top_k: int = 3,
    ) -> List[Dict]:

        results = []

        for (
            concept_name,
            concept_data,
        ) in self.concepts.items():

            score = self.cosine_similarity(
                chunk_embedding,
                concept_data["embedding"],
            )

            results.append({
                "concept": concept_name,
                "score": round(
                    float(score),
                    4,
                ),
            })

        results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return results[:top_k]