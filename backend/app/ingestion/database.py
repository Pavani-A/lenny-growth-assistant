from datetime import datetime, timezone

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models.episode import Episode
from app.models.transcript_chunk import TranscriptChunk


def upsert_episode(
    db: Session,
    metadata: dict,
) -> Episode:
    """Create a new episode or update an existing episode by filename."""

    episode = (
        db.query(Episode)
        .filter(Episode.filename == metadata["filename"])
        .first()
    )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    if episode is None:
        episode = Episode(
            title=metadata["title"],
            guest=metadata.get("guest"),
            description=metadata.get("description"),
            published_date=metadata.get("published_date"),
            source_url=metadata.get("source_url"),
            youtube_url=metadata.get("youtube_url"),
            filename=metadata["filename"],
            word_count=metadata.get("word_count"),
            created_at=now,
            updated_at=now,
        )

        db.add(episode)
        db.flush()

    else:
        episode.title = metadata["title"]
        episode.guest = metadata.get("guest")
        episode.description = metadata.get("description")
        episode.published_date = metadata.get("published_date")
        episode.source_url = metadata.get("source_url")
        episode.youtube_url = metadata.get("youtube_url")
        episode.word_count = metadata.get("word_count")
        episode.updated_at = now

        db.flush()

        db.execute(
            delete(TranscriptChunk).where(
                TranscriptChunk.episode_id == episode.id
            )
        )

    return episode


def add_transcript_chunks(
    db: Session,
    episode: Episode,
    chunks: list[str],
    embeddings: list[list[float]],
) -> None:
    """Store transcript chunks and their embeddings for an episode."""

    if len(chunks) != len(embeddings):
        raise ValueError(
            "The number of chunks must match the number of embeddings."
        )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    for index, (content, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        transcript_chunk = TranscriptChunk(
            episode_id=episode.id,
            chunk_index=index,
            content=content,
            embedding=embedding,
            created_at=now,
        )

        db.add(transcript_chunk)