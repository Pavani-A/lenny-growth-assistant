from app.db.database import SessionLocal
from app.embeddings.ollama_embeddings import OllamaEmbeddingService
from app.models.episode import Episode
from app.models.transcript_chunk import TranscriptChunk


DEFAULT_TOP_K = 5


def search_transcripts(
    query: str,
    top_k: int = DEFAULT_TOP_K,
) -> list[dict]:
    """Search transcript chunks using vector similarity."""

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    embedding_service = OllamaEmbeddingService()

    query_embedding = embedding_service.embed_text(query)

    db = SessionLocal()

    try:
        distance = TranscriptChunk.embedding.cosine_distance(
            query_embedding
        )

        results = (
            db.query(
                TranscriptChunk,
                Episode,
                distance.label("distance"),
            )
            .join(
                Episode,
                TranscriptChunk.episode_id == Episode.id,
            )
            .filter(
                TranscriptChunk.embedding.is_not(None)
            )
            .order_by(distance)
            .limit(top_k)
            .all()
        )

        return [
            {
                "chunk_id": chunk.id,
                "episode_id": episode.id,
                "episode_title": episode.title,
                "guest": episode.guest,
                "published_date": episode.published_date,
                "source_url": episode.source_url,
                "youtube_url": episode.youtube_url,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "distance": float(distance),
            }
            for chunk, episode, distance in results
        ]

    finally:
        db.close()