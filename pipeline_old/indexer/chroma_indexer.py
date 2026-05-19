from chromadb import PersistentClient


class ChromaIndexer:
    def __init__(self, path="./chroma_db"):
        self.client = PersistentClient(path=path)

        self.collection = self.client.get_or_create_collection(
            name="code_chunks"
        )

    def add_chunk(self, chunk, embedding):
        metadata = {
            "type": str(chunk.get("type", "")),
            "name": str(chunk.get("name", "")),
            "file": str(chunk.get("file", "")),
            "code": str(chunk.get("code", "")),
            "start_line": str(chunk.get("start_line", "")),
            "end_line": str(chunk.get("end_line", "")),
            "symbol_path": str(chunk.get("symbol_path", "")),
            "semantic_type": str(chunk.get("semantic_type", "")),
            "semantic_top_concept": str(
                chunk.get("semantic_top_concept", "")
            ),
            "semantic_confidence": float(
                chunk.get("semantic_confidence", 0.0)
            ),
            "importance_score": float(
                chunk.get("importance_score", 1.0)
            ),
            "chunk_id": str(chunk.get("chunk_id", "")),
            "parent_chunk_id": str(
                chunk.get("parent_chunk_id", "")
            ),
            "parent_class": str(chunk.get("parent_class", "")),
            "module_name": str(chunk.get("module_name", "")),
            "ast_hierarchy_path": str(
                chunk.get("ast_hierarchy_path", "")
            ),
            "decorators": str(chunk.get("decorators", "")),
            "imports_context": str(
                chunk.get("imports_context", "")
            ),
            "siblings": str(chunk.get("siblings", "")),
            "semantic_matches": str(
                chunk.get("semantic_matches", "")
            ),
        }

        self.collection.add(
            ids=[chunk["chunk_id"]],
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[chunk["code"]],
        )

    def search(self, embedding, top_k=5):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

    def reset(self):
        self.client.delete_collection("code_chunks")

        self.collection = self.client.get_or_create_collection(
            name="code_chunks"
        )