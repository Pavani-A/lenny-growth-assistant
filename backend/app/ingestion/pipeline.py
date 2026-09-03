from pathlib import Path

from app.db.database import SessionLocal
from app.embeddings.ollama_embeddings import OllamaEmbeddingService
from app.ingestion.chunker import chunk_text
from app.ingestion.database import add_transcript_chunks, upsert_episode
from app.ingestion.parser import (
    load_index,
    load_transcript_content,
    parse_podcast_metadata,
)


REPOSITORY_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "lenny-transcripts"
)


def ingest_episode(
    podcast_index: int = 0,
) -> None:
    """Ingest one podcast transcript into PostgreSQL."""

    items = load_index(REPOSITORY_PATH)

    if podcast_index < 0 or podcast_index >= len(items):
        raise IndexError(
            f"Podcast index {podcast_index} is out of range. "
            f"Available podcasts: {len(items)}."
        )

    item = items[podcast_index]

    metadata = parse_podcast_metadata(item)

    transcript = load_transcript_content(
        REPOSITORY_PATH,
        metadata["filename"],
    )

    chunks = chunk_text(transcript)

    if not chunks:
        raise ValueError(
            f"No transcript chunks found for {metadata['filename']}."
        )

    print(f"Episode: {metadata['title']}")
    print(f"Chunks: {len(chunks)}")
    print("Generating embeddings...")

    embedding_service = OllamaEmbeddingService()

    embeddings = embedding_service.embed_texts(chunks)

    if len(embeddings) != len(chunks):
        raise ValueError(
            "The number of embeddings does not match the number of chunks."
        )

    print(f"Generated {len(embeddings)} embeddings.")

    print("Saving episode and chunks to PostgreSQL...")

    db = SessionLocal()

    try:
        episode = upsert_episode(
            db=db,
            metadata=metadata,
        )

        add_transcript_chunks(
            db=db,
            episode=episode,
            chunks=chunks,
            embeddings=embeddings,
        )

        db.commit()

        print("Ingestion successful.")
        print(f"Episode ID: {episode.id}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
def ingest_all_episodes() -> None:
    """Ingest all podcast transcripts from the knowledge base."""

    items = load_index(REPOSITORY_PATH)

    total = len(items)

    print(f"Found {total} podcast transcripts.")

    for index in range(total):
        print()
        print("=" * 70)
        print(f"Processing episode {index + 1}/{total}")
        print("=" * 70)

        ingest_episode(index)

    print()
    print("=" * 70)
    print(f"All {total} episodes ingested successfully.")
    print("=" * 70)