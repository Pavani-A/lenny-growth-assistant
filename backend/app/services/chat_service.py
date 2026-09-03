from collections.abc import Iterator

from app.agent.ollama_agent import OllamaGrowthAssistantAgent
from app.schemas.chat import ChatResponse


class ChatService:
    """Service responsible for processing chat requests."""

    def __init__(self):
        self.ollama_agent = OllamaGrowthAssistantAgent()

    def chat(
        self,
        message: str,
        session_id: str,
        provider: str,
    ) -> ChatResponse:
        """Process a chat request using the selected provider."""

        if provider != "ollama":
            raise ValueError(
                f"Provider '{provider}' is not available yet."
            )

        result = self.ollama_agent.run(
            message=message,
            session_id=session_id,
        )

        sources = [
            {
                "episode_title": source["episode_title"],
                "guest": source["guest"],
                "published_date": (
                    source["published_date"].isoformat()
                    if source["published_date"]
                    else None
                ),
                "source_url": source["source_url"],
                "youtube_url": source["youtube_url"],
                "chunk_index": source["chunk_index"],
                "content": source["content"],
                "distance": source["distance"],
            }
            for source in result.sources
        ]

        return ChatResponse(
            session_id=session_id,
            provider=provider,
            answer=result.answer,
            sources=sources,
        )

    def chat_stream(
        self,
        message: str,
        session_id: str,
        provider: str,
    ) -> tuple[Iterator[str], list[dict]]:
        """Process a chat request and stream the assistant response."""

        if provider != "ollama":
            raise ValueError(
                f"Provider '{provider}' is not available for streaming yet."
            )

        return self.ollama_agent.run_stream(
            message=message,
            session_id=session_id,
        )