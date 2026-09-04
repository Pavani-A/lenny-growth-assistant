from app.retrieval.search import search_transcripts


def build_grounded_context(
    query: str,
    top_k: int = 5,
) -> tuple[str, list[dict]]:
    """Retrieve relevant transcript chunks and format them for the agent."""

    results = search_transcripts(query, top_k=top_k)

    if not results:
        return "", []

    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"""SOURCE {index}
Episode: {result["episode_title"]}
Guest: {result["guest"]}
Published: {result["published_date"]}
YouTube: {result["youtube_url"]}
Transcript:
{result["content"]}
"""
        )

    return "\n\n".join(context_parts), results