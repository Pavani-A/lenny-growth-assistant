from datetime import datetime

from pydantic import BaseModel


class ConversationSummary(BaseModel):
    """Summary shown in the conversation sidebar."""

    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationMessageResponse(BaseModel):
    """A message returned when loading a conversation."""

    role: str
    content: str
    created_at: datetime


class ConversationDetail(BaseModel):
    """Full conversation returned when a session is opened."""

    session_id: str
    user_id: str | None
    created_at: datetime
    updated_at: datetime
    messages: list[ConversationMessageResponse]