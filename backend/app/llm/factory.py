from app.llm.base import LLMProvider
from app.llm.claude_provider import ClaudeProvider
from app.llm.ollama import OllamaProvider
from app.llm.openai_provider import OpenAIProvider


def get_llm_provider(provider: str) -> LLMProvider:
    """Return the configured LLM provider."""

    normalized_provider = provider.strip().lower()

    if normalized_provider == "ollama":
        return OllamaProvider()

    if normalized_provider == "openai":
        return OpenAIProvider()

    if normalized_provider == "claude":
        return ClaudeProvider()

    raise ValueError(
        f"Unsupported provider '{provider}'. "
        "Choose one of: ollama, openai, claude."
    )