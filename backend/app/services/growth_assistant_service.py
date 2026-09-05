from collections.abc import Iterator

from app.agent.grounded_agent import GroundedLennyAgent
from app.db.database import SessionLocal
from app.repositories.conversation_repository import ConversationRepository


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
        self.conversation_repository = ConversationRepository()

    def _build_conversation_history(
        self,
        messages: list,
    ) -> str:
        """Format previous messages for the Pi Agent prompt."""

        if not messages:
            return ""

        history_parts = []

        for message in messages:
            role = "User" if message.role == "user" else "Assistant"

            history_parts.append(
                f"{role}: {message.content}"
            )

        return "\n".join(history_parts)

    def _build_retrieval_query(
        self,
        messages: list,
        current_message: str,
    ) -> str:
        """Build a retrieval query using recent user messages."""

        recent_user_messages = [
            message.content
            for message in messages
            if message.role == "user"
        ][-2:]

        if not recent_user_messages:
            return current_message

        return "\n".join(
            recent_user_messages + [current_message]
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
        session_id: str,
        top_k: int = 5,
    ) -> tuple[Iterator[str], list[dict]]:
        """Stream a grounded answer and persist the conversation."""

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        if not session_id.strip():
            raise ValueError("Session ID cannot be empty.")

        db = SessionLocal()

        try:
            conversation = (
                self.conversation_repository.get_or_create_conversation(
                    db=db,
                    session_id=session_id,
                    user_id=None,
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

            retrieval_query = self._build_retrieval_query(
                messages=previous_messages,
                current_message=message,
            )

            self.conversation_repository.add_message(
                db=db,
                conversation_id=conversation.id,
                role="user",
                content=message,
            )

            stream, sources = self.agent.stream_answer(
                question=message,
                top_k=top_k,
                conversation_history=conversation_history,
                retrieval_query=retrieval_query,
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