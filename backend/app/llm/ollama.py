import os
from collections.abc import Iterator

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
    "llama3.2:3b",
)

OLLAMA_TIMEOUT = float(
    os.getenv(
        "OLLAMA_TIMEOUT",
        "120",
    )
)


class OllamaProvider(LLMProvider):
    """Ollama implementation of the common LLM provider interface."""

    def __init__(self):
        self.client = ollama.Client(
            host=OLLAMA_BASE_URL,
            timeout=OLLAMA_TIMEOUT,
        )

    def _build_messages(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> list[dict[str, str]]:
        """Build messages shared by normal and streaming generation."""

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        messages: list[dict[str, str]] = []

        if system_prompt and system_prompt.strip():
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

        return messages

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a complete response from Ollama."""

        messages = self._build_messages(
            prompt,
            system_prompt,
        )

        try:
            response = self.client.chat(
                model=OLLAMA_MODEL,
                messages=messages,
            )

        except Exception as exc:
            raise RuntimeError(
                f"Ollama generation failed using model "
                f"'{OLLAMA_MODEL}': {exc}"
            ) from exc

        content = response["message"]["content"]

        if not content or not content.strip():
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        return content

    def generate_stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> Iterator[str]:
        """Generate a response from Ollama incrementally."""

        messages = self._build_messages(
            prompt,
            system_prompt,
        )

        try:
            response = self.client.chat(
                model=OLLAMA_MODEL,
                messages=messages,
                stream=True,
            )

            for chunk in response:
                content = chunk["message"]["content"]

                if content:
                    yield content

        except Exception as exc:
            raise RuntimeError(
                f"Ollama streaming failed using model "
                f"'{OLLAMA_MODEL}': {exc}"
            ) from exc