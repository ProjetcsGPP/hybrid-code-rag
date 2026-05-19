from vectordb import search

from pipeline.ranking.hybrid_ranker import (
    HybridRanker,
)
from pipeline.intent.intent_classifier import detect_intent
from pipeline.contracts import ChunkResult


class HybridRetriever:

    def __init__(
        self,
        embedding_service,
        semantic_registry,
    ):

        self.embedding_service = (
            embedding_service
        )

        self.semantic_registry = (
            semantic_registry
        )

        self.ranker = HybridRanker()

    def retrieve(
        self,
        query,
        k=5,
        candidate_k=25,
    ):

        intent = detect_intent(query)
        
        q_emb = (
            self.embedding_service
            .generate_embedding(query)
        )

        query_semantic_matches = (
            self.semantic_registry
            .find_similar_concepts(q_emb)
        )

        query_top_concept = None

        if query_semantic_matches:

            query_top_concept = (
                query_semantic_matches[0][
                    "concept"
                ]
            )
            
        # candidate expansion
        results = search(
            q_emb,
            k=candidate_k,
        )

        docs = results["documents"][0]
        meta = results["metadatas"][0]
        dist = results["distances"][0]

        ranker_input: list[dict] = []

        for i in range(len(docs)):

            metadata = meta[i]

            base_distance = dist[i]
            vector_similarity = 1 - base_distance

            semantic_alignment = 0.0

            semantic_top_concept = metadata.get("semantic_top_concept", "")
            semantic_confidence = float(metadata.get("semantic_confidence", 0.0))

            if query_top_concept and semantic_top_concept == query_top_concept:
                semantic_alignment = semantic_confidence
            
            ranker_input.append({
                "doc": docs[i],
                "meta": {
                    **metadata,
                    "name": metadata.get("name", "")
                },

                "vector_score": vector_similarity,
                "semantic_score": semantic_alignment,
                "structural_score": 0.0,   # ainda não usado aqui
                "importance_score": float(metadata.get("importance_score", 1.0)),
                "intent_score": 0.0,       # preenchido no ranker
            })            
            
        ranked = self.ranker.rank(
            query=query,
            results=ranker_input,
        )

        normalized = []

        for r in ranked:
          
            normalized.append({

                "final_score": r["final_score"],

                "vector_score": r["vector_score"],
                "semantic_score": r["semantic_score"],
                "structural_score": r["structural_score"],
                "intent_score": r["intent_score"],

                "importance": r["importance_score"],

                "normalized_importance": min(
                    r["importance_score"] / 2.0,
                    1.0
                ),

                "meta": r["meta"],
                "doc": r["doc"],
            })

        return normalized[:k]