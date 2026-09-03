from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Common interface for all LLM providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a text response from the model."""
        raise NotImplementedError