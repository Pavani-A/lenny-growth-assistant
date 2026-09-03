from app.retrieval.search import search_transcripts


def build_retrieval_context(
    query: str,
    top_k: int = 5,
    max_words_per_source: int = 500,
) -> tuple[str, list[dict]]:
    """Retrieve transcript chunks and format them for the agent."""

    results = search_transcripts(query, top_k=top_k)

    if not results:
        return "", []

    context_parts = []

    for index, result in enumerate(results, start=1):
        transcript_excerpt = " ".join(
            result["content"].split()[:max_words_per_source]
        )

        context_parts.append(
            f"""Source {index}
Episode: {result["episode_title"]}
Guest: {result["guest"] or "Unknown"}
Published: {result["published_date"] or "Unknown"}
Source URL: {result["source_url"] or "Unavailable"}

Transcript:
{transcript_excerpt}
"""
        )

    return "\n\n---\n\n".join(context_parts), results