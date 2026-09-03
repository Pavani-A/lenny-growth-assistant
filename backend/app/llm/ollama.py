import os

import ollama
from dotenv import load_dotenv

from app.llm.base import LLMProvider


load_dotenv()


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2",
)


class OllamaProvider(LLMProvider):
    """Generate responses using a local Ollama model."""

    def __init__(self) -> None:
        self.client = ollama.Client(
            host=OLLAMA_BASE_URL,
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.chat(
            model=OLLAMA_MODEL,
            messages=messages,
        )

        return response["message"]["content"]