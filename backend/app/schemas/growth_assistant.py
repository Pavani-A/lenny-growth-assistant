from datetime import date

from pydantic import BaseModel, Field


class GrowthAssistantRequest(BaseModel):
    """Request body for the Pi-based Growth Assistant."""

    message: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=10)


class GrowthAssistantSource(BaseModel):
    """Transcript source returned by the assistant."""

    episode_title: str
    guest: str
    published_date: date | None = None
    source_url: str | None = None
    youtube_url: str | None = None
    chunk_index: int
    content: str
    distance: float


class GrowthAssistantResponse(BaseModel):
    """Response returned by the Pi-based Growth Assistant."""

    answer: str
    sources: list[GrowthAssistantSource]

class Ship30Request(BaseModel):
    """Request body for Ship 30 for 30 article generation."""

    topic: str = Field(min_length=1)


class Ship30Response(BaseModel):
    """Response returned by the Ship 30 for 30 generator."""

    article: str
    sources: list[GrowthAssistantSource]
    word_count: int