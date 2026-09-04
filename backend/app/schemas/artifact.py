from typing import Literal

from pydantic import BaseModel, Field


class Artifact(BaseModel):
    """Generated artifact returned by the growth assistant."""

    type: Literal["html", "markdown"]
    title: str = Field(
        min_length=1,
        description="Human-readable artifact title.",
    )
    content: str = Field(
        min_length=1,
        description="Artifact content.",
    )


class ArtifactRequest(BaseModel):
    """Request to generate an artifact."""

    prompt: str = Field(
        min_length=1,
        description="Description of the artifact the user wants.",
    )
    session_id: str = Field(
        min_length=1,
        description="Conversation session identifier.",
    )
    user_id: str | None = Field(
        default=None,
        description="Optional user identifier.",
    )
    provider: str = Field(
        default="ollama",
        description="LLM provider to use.",
    )


class ArtifactResponse(BaseModel):
    """API response containing a generated artifact."""

    session_id: str
    provider: str
    artifact: Artifact