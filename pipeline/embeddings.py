import requests
import numpy as np


OLLAMA_URL = (
    "http://localhost:11434/api/embeddings"
)

MODEL = "nomic-embed-text"


class EmbeddingService:

    def __init__(
        self,
        model=MODEL,
        ollama_url=OLLAMA_URL,
    ):
        self.model = model
        self.ollama_url = ollama_url

    def normalize(self, vector):

        vector = np.array(
            vector,
            dtype=np.float32,
        )

        norm = np.linalg.norm(vector)

        if norm == 0:
            return vector.tolist()

        return (vector / norm).tolist()

    def generate_embedding(
        self,
        text: str,
    ):

        response = requests.post(
            self.ollama_url,
            json={
                "model": self.model,
                "prompt": text,
            },
        )

        response.raise_for_status()

        data = response.json()

        embedding = data.get(
            "embedding"
        )

        # fallback compatibilidade
        if embedding is None:

            embeddings = data.get(
                "embeddings"
            )

            if embeddings:
                embedding = embeddings[0]

        if not embedding:

            raise RuntimeError(
                "Ollama retornou embedding "
                f"inválido: {data}"
            )

        return self.normalize(
            embedding
        )

    # 🔥 embeddings conceituais
    # separados semanticamente
    # para futura evolução
    def generate_concept_embedding(
        self,
        concept_text: str,
    ):
        return self.generate_embedding(
            concept_text
        )