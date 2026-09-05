from collections.abc import Iterator

from app.agent.grounded_agent import GroundedLennyAgent


class GrowthAssistantService:
    """Service for the Pi-based Lenny Growth Assistant flow."""

    def __init__(
        self,
        provider: str = "ollama",
        model: str = "llama3.2:3b",
    ):
        self.agent = GroundedLennyAgent(
            provider=provider,
            model=model,
        )

    def answer(
        self,
        message: str,
        top_k: int = 5,
    ) -> tuple[str, list[dict]]:
        """Generate a grounded answer using the Pi-based agent."""

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        result = self.agent.answer(
            question=message,
            top_k=top_k,
        )

        return result.answer, result.sources

    def stream_answer(
        self,
        message: str,
        top_k: int = 5,
    ) -> tuple[Iterator[str], list[dict]]:
        """Stream a grounded answer using the Pi-based agent."""

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        stream, sources = self.agent.stream_answer(
            question=message,
            top_k=top_k,
        )

        return stream, sources