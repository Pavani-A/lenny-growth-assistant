import os

from anthropic import Anthropic
from dotenv import load_dotenv

from app.llm.base import LLMProvider


load_dotenv()


class ClaudeProvider(LLMProvider):
    """Anthropic Claude implementation of the common LLM provider interface."""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key or not api_key.strip():
            raise ValueError(
                "Claude API key is not configured. "
                "Please add ANTHROPIC_API_KEY to your .env file."
            )

        self.client = Anthropic(api_key=api_key)

        self.model = os.getenv(
            "ANTHROPIC_MODEL",
            "claude-3-5-haiku-latest",
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt or "",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        except Exception as exc:
            raise RuntimeError(
                f"Claude generation failed using model "
                f"'{self.model}': {exc}"
            ) from exc

        content_parts = []

        for block in response.content:
            if getattr(block, "type", None) == "text":
                content_parts.append(block.text)

        content = "".join(content_parts)

        if not content.strip():
            raise RuntimeError(
                "Claude returned an empty response."
            )

        return content