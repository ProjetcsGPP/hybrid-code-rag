from pipeline.semantic.semantic_matcher import SemanticMatcher


class Retriever:

    def __init__(self, chroma_indexer):
        self.chroma = chroma_indexer
        self.semantic_matcher = SemanticMatcher()

    def search(self, query_embedding, query_text, top_k=5):

        results = self.chroma.search(query_embedding, top_k)

        query_semantics = (
            self.semantic_matcher.extract_query_semantics(
                query_text
            )
        )

        query_top_concepts = {
            item["concept"]
            for item in query_semantics
        }

        print("\n🎯 SYMBOLIC TARGETS")
        print(query_top_concepts)

        ranked = []

        for i in range(len(results["ids"][0])):

            metadata = results["metadatas"][0][i]

            base_distance = results["distances"][0][i]

            vector_similarity = max(0.0, 1 - base_distance)

            semantic_type = metadata.get(
                "semantic_type",
                "general",
            )

            semantic_top_concept = metadata.get(
                "semantic_top_concept",
                ""
            )

            semantic_confidence = float(
                metadata.get(
                    "semantic_confidence",
                    0.0
                )
            )

            importance = float(
                metadata.get(
                    "importance_score",
                    1.0
                )
            )

            normalized_importance = min(
                importance / 2.0,
                1.0
            )

            semantic_alignment = 0.0

            if semantic_top_concept in query_top_concepts:
                semantic_alignment = semantic_confidence

            symbolic_boost = 0.0

            if semantic_type in query_top_concepts:
                symbolic_boost = 0.25

            final_score = (
                (vector_similarity * 0.55)
                + (semantic_alignment * 0.25)
                + (normalized_importance * 0.10)
                + (symbolic_boost * 0.10)
            )

            print("\n🧪 DEBUG CHUNK")
            print(f"FILE: {metadata.get('file')}")
            print(f"NAME: {metadata.get('name')}")
            print(f"TYPE: {metadata.get('type')}")
            print(f"CHUNK_ID: {metadata.get('chunk_id')}")
            print(f"SEMANTIC_TYPE: {semantic_type}")
            print(f"SEMANTIC_TOP_CONCEPT: {semantic_top_concept}")
            print(f"SEMANTIC_CONFIDENCE: {semantic_confidence}")
            print(f"SEMANTIC_ALIGNMENT: {semantic_alignment}")
            print(f"SYMBOLIC_BOOST: {symbolic_boost}")
            print(f"IMPORTANCE: {importance}")
            print(f"NORMALIZED_IMPORTANCE: {normalized_importance}")
            print(f"BASE_DISTANCE: {base_distance}")
            print(f"VECTOR_SIMILARITY: {vector_similarity}")
            print(f"FINAL_SCORE: {final_score}")

            ranked.append({

                "score": final_score,
                "vector_similarity": vector_similarity,
                "semantic_alignment": semantic_alignment,
                "symbolic_boost": symbolic_boost,

                "semantic_confidence": semantic_confidence,
                "importance": importance,
                "normalized_importance": normalized_importance,

                "metadata": metadata,
                "meta": metadata,
            })

        ranked.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked