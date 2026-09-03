from collections.abc import Iterator

from app.agent.ollama_agent import OllamaGrowthAssistantAgent
from app.db.database import SessionLocal
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.chat import ChatResponse


class ChatService:
    """Service responsible for processing chat requests."""

    def __init__(self):
        self.ollama_agent = OllamaGrowthAssistantAgent()
        self.conversation_repository = ConversationRepository()

    def _build_conversation_history(
        self,
        messages: list,
    ) -> str:
        """Format previous messages for the agent prompt."""

        if not messages:
            return ""

        history_parts = []

        for message in messages:
            role = "User" if message.role == "user" else "Assistant"

            history_parts.append(
                f"{role}: {message.content}"
            )

        return "\n".join(history_parts)

    def chat(
        self,
        message: str,
        session_id: str,
        provider: str,
        user_id: str | None = None,
    ) -> ChatResponse:
        """Process a chat request using the selected provider."""

        if provider != "ollama":
            raise ValueError(
                f"Provider '{provider}' is not available yet."
            )

        db = SessionLocal()

        try:
            conversation = (
                self.conversation_repository.get_or_create_conversation(
                    db=db,
                    session_id=session_id,
                    user_id=user_id,
                )
            )

            previous_messages = (
                self.conversation_repository.get_messages(
                    db=db,
                    conversation_id=conversation.id,
                )
            )

            conversation_history = self._build_conversation_history(
                previous_messages
            )

            self.conversation_repository.add_message(
                db=db,
                conversation_id=conversation.id,
                role="user",
                content=message,
            )

            result = self.ollama_agent.run(
                message=message,
                session_id=session_id,
                conversation_history=conversation_history,
            )

            self.conversation_repository.add_message(
                db=db,
                conversation_id=conversation.id,
                role="assistant",
                content=result.answer,
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

        finally:
            db.close()

    def chat_stream(
        self,
        message: str,
        session_id: str,
        provider: str,
        user_id: str | None = None,
    ) -> tuple[Iterator[str], list[dict]]:
        """Process a chat request and stream the assistant response."""

        if provider != "ollama":
            raise ValueError(
                f"Provider '{provider}' is not available for streaming yet."
            )

        db = SessionLocal()

        try:
            conversation = (
                self.conversation_repository.get_or_create_conversation(
                    db=db,
                    session_id=session_id,
                    user_id=user_id,
                )
            )

            previous_messages = (
                self.conversation_repository.get_messages(
                    db=db,
                    conversation_id=conversation.id,
                )
            )

            conversation_history = self._build_conversation_history(
                previous_messages
            )

            self.conversation_repository.add_message(
                db=db,
                conversation_id=conversation.id,
                role="user",
                content=message,
            )

            stream, sources = self.ollama_agent.run_stream(
                message=message,
                session_id=session_id,
                conversation_history=conversation_history,
            )

            def tracked_stream() -> Iterator[str]:
                assistant_chunks = []

                try:
                    for chunk in stream:
                        assistant_chunks.append(chunk)
                        yield chunk

                    assistant_answer = "".join(assistant_chunks)

                    if assistant_answer.strip():
                        self.conversation_repository.add_message(
                            db=db,
                            conversation_id=conversation.id,
                            role="assistant",
                            content=assistant_answer,
                        )

                finally:
                    db.close()

            return tracked_stream(), sources

        except Exception:
            db.close()
            raise