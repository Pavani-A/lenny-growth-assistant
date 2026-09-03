from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.conversation_message import ConversationMessage


class ConversationRepository:
    """Database operations for conversation sessions and messages."""

    def get_or_create_conversation(
        self,
        db: Session,
        session_id: str,
        user_id: str | None = None,
    ) -> Conversation:
        """Return an existing conversation or create a new one."""

        conversation = (
            db.query(Conversation)
            .filter(Conversation.session_id == session_id)
            .first()
        )

        if conversation:
            if user_id is not None and conversation.user_id != user_id:
                conversation.user_id = user_id
                db.commit()
                db.refresh(conversation)

            return conversation

        conversation = Conversation(
            session_id=session_id,
            user_id=user_id,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def add_message(
        self,
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
    ) -> ConversationMessage:
        """Store a message in a conversation."""

        if role not in {"user", "assistant"}:
            raise ValueError(
                "Message role must be either 'user' or 'assistant'."
            )

        if not content.strip():
            raise ValueError("Message content cannot be empty.")

        message = ConversationMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)

        conversation = db.get(
            Conversation,
            conversation_id,
        )

        if conversation:
            conversation.updated_at = datetime.now(UTC)

        db.commit()
        db.refresh(message)

        return message

    def get_messages(
        self,
        db: Session,
        conversation_id: int,
    ) -> list[ConversationMessage]:
        """Return messages in chronological order."""

        return (
            db.query(ConversationMessage)
            .filter(
                ConversationMessage.conversation_id
                == conversation_id
            )
            .order_by(ConversationMessage.created_at.asc())
            .all()
        )