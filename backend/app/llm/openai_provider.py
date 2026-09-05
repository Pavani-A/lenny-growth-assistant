import os

from dotenv import load_dotenv
from openai import OpenAI

from app.llm.base import LLMProvider


load_dotenv()


class OpenAIProvider(LLMProvider):
    """OpenAI implementation of the common LLM provider interface."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key or not api_key.strip():
            raise ValueError(
                "OpenAI API key is not configured. "
                "Please add OPENAI_API_KEY to your .env file."
            )

        self.client = OpenAI(api_key=api_key)

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini",
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
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

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
        except Exception as exc:
            raise RuntimeError(
                f"OpenAI generation failed using model "
                f"'{self.model}': {exc}"
            ) from exc

        content = response.choices[0].message.content

        if not content or not content.strip():
            raise RuntimeError(
                "OpenAI returned an empty response."
            )

        return content