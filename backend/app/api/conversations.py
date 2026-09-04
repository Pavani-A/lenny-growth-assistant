from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.conversation import Conversation


router = APIRouter(
    prefix="/api/v1/conversations",
    tags=["conversations"],
)


def build_conversation_title(conversation: Conversation) -> str:
    """Create a sidebar title from the first user message."""

    for message in conversation.messages:
        if message.role == "user":
            text = message.content.strip()

            if len(text) <= 45:
                return text

            return text[:42].rstrip() + "..."

    return "New conversation"


@router.get("")
def list_conversations() -> list[dict]:
    """Return conversations for the sidebar."""

    db: Session = SessionLocal()

    try:
        conversations = (
             db.query(Conversation)
            .join(Conversation.messages)
            .distinct()
            .order_by(Conversation.updated_at.desc())
            .all()
        )

        return [
            {
                "session_id": conversation.session_id,
                "title": build_conversation_title(conversation),
                "created_at": conversation.created_at,
                "updated_at": conversation.updated_at,
            }
            for conversation in conversations
        ]

    finally:
        db.close()


@router.get("/{session_id}")
def get_conversation(session_id: str) -> dict:
    """Return one conversation and its messages."""

    db: Session = SessionLocal()

    try:
        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.session_id == session_id,
            )
            .first()
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "conversation_not_found",
                    "message": "Conversation was not found.",
                },
            )

        return {
            "session_id": conversation.session_id,
            "user_id": conversation.user_id,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                    "created_at": message.created_at,
                }
                for message in conversation.messages
            ],
        }

    finally:
        db.close()