import os

import ollama
from dotenv import load_dotenv


load_dotenv()


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

EMBEDDING_MODEL = os.getenv(
    "OLLAMA_EMBEDDING_MODEL",
    "embeddinggemma",
)


class OllamaEmbeddingService:
    """Generate embeddings using a local Ollama model."""

    def __init__(self) -> None:
        self.client = ollama.Client(
            host=OLLAMA_BASE_URL,
        )

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding for a single text string."""
        if not text.strip():
            raise ValueError(
                "Cannot generate an embedding for empty text."
            )

        response = self.client.embed(
            model=EMBEDDING_MODEL,
            input=text,
        )

        return response["embeddings"][0]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple text strings."""
        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError(
                "Cannot generate embeddings for empty text."
            )

        response = self.client.embed(
            model=EMBEDDING_MODEL,
            input=texts,
        )

        return response["embeddings"]