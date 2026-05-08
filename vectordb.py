# vectordb.py
import chromadb
from config import DB_PATH

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("codebase")


def reset_collection():
    """
    🔥 USE ISSO DURANTE DESENVOLVIMENTO
    Limpa completamente o índice para evitar dados antigos.
    """
    try:
        client.delete_collection("codebase")
    except Exception:
        pass

    global collection
    collection = client.get_or_create_collection("codebase")


def add_embedding(id, embedding, metadata, text):
    # 🔥 garante compatibilidade total com Chroma
    safe_metadata = {
        k: (str(v) if not isinstance(v, (int, float, bool)) else v)
        for k, v in metadata.items()
    }

    collection.add(
        ids=[id],
        embeddings=[embedding],
        metadatas=[safe_metadata],
        documents=[text]
    )


def search(query_embedding, k=5):
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    return result