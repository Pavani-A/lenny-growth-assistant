from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    message: str = Field(
        min_length=1,
        description="User's message to the growth assistant.",
    )
    session_id: str = Field(
        min_length=1,
        description="Conversation session identifier.",
    )
    provider: str = Field(
        default="ollama",
        description="LLM provider to use.",
    )


class ChatSource(BaseModel):
    """Transcript source returned with an assistant response."""

    episode_title: str
    guest: str | None = None
    published_date: str | None = None
    source_url: str | None = None
    youtube_url: str | None = None
    chunk_index: int
    content: str
    distance: float


class ChatResponse(BaseModel):
    """Response returned by the chat endpoint."""

    session_id: str
    provider: str
    answer: str
    sources: list[ChatSource]