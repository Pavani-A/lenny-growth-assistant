from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Episode(Base):
    __tablename__ = "episodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    guest: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    published_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    youtube_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
    )

    word_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    chunks = relationship(
        "TranscriptChunk",
        back_populates="episode",
        cascade="all, delete-orphan",
    )