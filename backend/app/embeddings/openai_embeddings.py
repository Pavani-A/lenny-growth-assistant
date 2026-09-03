import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


EMBEDDING_MODEL = "text-embedding-3-small"


class OpenAIEmbeddingService:
    """Generate embeddings using OpenAI."""

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(api_key=api_key)

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding for a single text string."""
        if not text.strip():
            raise ValueError("Cannot generate an embedding for empty text.")

        response = self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
        )

        return response.data[0].embedding