from pipeline.ast_chunker import ASTChunker
from pipeline.embeddings import EmbeddingService
from vectordb import add_embedding, reset_collection
from pipeline.semantic_registry import SemanticRegistry
from pipeline.retrieval.hybrid_retriever import HybridRetriever
from pipeline.contracts import ChunkMeta

import hashlib
import argparse


# ==========================================================
# ARGPARSE
# ==========================================================

parser = argparse.ArgumentParser()

parser.add_argument("--file", required=True, help="Arquivo Python para indexação")
parser.add_argument("--query", default="onde esse arquivo faz validação?")
parser.add_argument("--k", type=int, default=5)
parser.add_argument("--reset", action="store_true")

args = parser.parse_args()

TEST_FILE = args.file


# ==========================================================
# HELPERS
# ==========================================================

def file_id(chunk):
    return hashlib.md5(
        chunk["metadata"]["chunk_id"].encode()
    ).hexdigest()


# ==========================================================
# SERVICES
# ==========================================================

embeddings = EmbeddingService()

semantic_registry = SemanticRegistry(
    embedding_service=embeddings
)

semantic_registry.load_default_concepts()

retriever = HybridRetriever(
    embedding_service=embeddings,
    semantic_registry=semantic_registry,
)


# ==========================================================
# RESET
# ==========================================================

if args.reset:
    print("🧨 Resetando collection...")
    reset_collection()


# ==========================================================
# AST CHUNKING
# ==========================================================

print("🔹 Lendo arquivo...")

chunks = ASTChunker(TEST_FILE).chunk()

print(f"🔹 Total de chunks: {len(chunks)}")


# ==========================================================
# INDEXAÇÃO
# ==========================================================

print("\n🔹 Indexando no ChromaDB...")

for chunk in chunks:

    print("\n================================")
    print(f"🔹 PROCESSANDO CHUNK: {chunk['metadata']['name']}")
    print("================================")

    emb = embeddings.generate_embedding(chunk["text"])

    # ------------------------------------------------------
    # SEMÂNTICA
    # ------------------------------------------------------

    semantic_matches = semantic_registry.find_similar_concepts(emb)

    chunk["metadata"].setdefault("semantic_matches", [])
    chunk["metadata"].setdefault("semantic_candidates", [])
    chunk["metadata"].setdefault("semantic_confidence", 0.0)
    chunk["metadata"].setdefault("semantic_top_concept", "unknown")

    if semantic_matches:

        top = semantic_matches[0]

        chunk["metadata"]["semantic_matches"] = semantic_matches
        chunk["metadata"]["semantic_confidence"] = float(top["score"])
        chunk["metadata"]["semantic_top_concept"] = top["concept"]

        chunk["metadata"]["semantic_candidates"] = [
            m["concept"] for m in semantic_matches
        ]

    else:
        chunk["metadata"]["semantic_confidence"] = 0.0
        chunk["metadata"]["semantic_top_concept"] = "unknown"
        chunk["metadata"]["semantic_candidates"] = []

    # ------------------------------------------------------
    # LOGS
    # ------------------------------------------------------

    for m in semantic_matches:
        print(f"[SEMANTIC] {m['concept']}={m['score']}")

    print(f"[CTX] chunk_id={chunk['metadata']['chunk_id']}")
    print(f"[CTX] parent_class={chunk['metadata']['parent_class']}")
    print(f"[CTX] decorators={chunk['metadata']['decorators']}")

    # ------------------------------------------------------
    # NORMALIZAÇÃO
    # ------------------------------------------------------

    meta: ChunkMeta = {
        "type": str(chunk["metadata"].get("type", "")),
        "name": str(chunk["metadata"].get("name", "")),
        "file": str(chunk["metadata"].get("file", "")),
        "chunk_id": str(chunk["metadata"].get("chunk_id", "")),

        "semantic_type": str(chunk["metadata"].get("semantic_type", "general")),
        "semantic_top_concept": str(chunk["metadata"].get("semantic_top_concept", "unknown")),
        "semantic_confidence": float(chunk["metadata"].get("semantic_confidence", 0.0)),
        "semantic_candidates": list(chunk["metadata"].get("semantic_candidates", [])),

        "importance_score": float(chunk["metadata"].get("importance_score", 1.0)),
    }

    print("\n🧪 CHUNK NORMALIZADO:")
    print(meta)

    # ------------------------------------------------------
    # INDEXAÇÃO
    # ------------------------------------------------------

    add_embedding(
        id=file_id(chunk),
        embedding=emb,
        metadata=meta,
        text=chunk["text"]
    )


print("\n✅ Indexação concluída")


# ==========================================================
# RETRIEVAL
# ==========================================================

print("\n🔹 Executando Hybrid Retrieval...")

results = retriever.retrieve(
    query=args.query,
    k=args.k,
    candidate_k=25,
)

for i, r in enumerate(results):
    print(f"\n=========== RESULT {i+1} ===========")
    print(type(r))
    print(r)

# ==========================================================
# RESULTADOS
# ==========================================================

for i, r in enumerate(results):

    meta = r.get("meta") or {}

    print(f"\n--- RANK {i+1} ---")

    print(f"FINAL_SCORE: {r.get('final_score', 0)}")
    print(f"VECTOR_SCORE: {r.get('vector_score', 0)}")
    print(f"SEMANTIC_SCORE: {r.get('semantic_score', 0)}")
    print(f"STRUCTURAL_SCORE: {r.get('structural_score', 0)}")
    print(f"INTENT_SCORE: {r.get('intent_score', 0)}")

    print(f"SEMANTIC_CONFIDENCE: {meta.get('semantic_confidence')}")
    print(f"IMPORTANCE: {r.get('importance', 0)}")
    print(f"NORMALIZED_IMPORTANCE: {r.get('normalized_importance', 0)}")

    print(f"FILE: {meta.get('file')}")
    print(f"TYPE: {meta.get('type')}")
    print(f"NAME: {meta.get('name')}")
    print(f"CHUNK_ID: {meta.get('chunk_id')}")
    print(f"SEMANTIC_TYPE: {meta.get('semantic_type')}")
    print(f"SEMANTIC_TOP_CONCEPT: {meta.get('semantic_top_concept')}")

    print("\nCODE:\n")
    print(r.get("doc", "")[:500])