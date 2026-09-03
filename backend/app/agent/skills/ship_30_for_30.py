from dataclasses import dataclass

from app.agent.context import build_retrieval_context


@dataclass
class Ship30For30Result:
    """Structured result produced by the Ship 30 for 30 skill."""

    article: str
    sources: list[dict]
    word_count: int


SHIP_30_FOR_30_SYSTEM_PROMPT = """
You are writing a Ship 30 for 30 style essay for the Lenny Growth Assistant.

Writing requirements:
- Aim for approximately 1,250 words.
- Start with a strong, curiosity-driven hook.
- Build a clear narrative from the source material.
- Use short paragraphs for readability.
- Use descriptive Markdown headings.
- Use bullet points when they improve skimmability.
- Use bold text to emphasize important ideas.
- Include specific, practical takeaways for the reader.
- Prefer concrete examples from the provided transcript material.
- Preserve the meaning and nuance of the source.
- Do not invent facts, quotes, examples, or claims.
- Do not present general knowledge as if it came from the transcript.
- If the available transcript material does not adequately support a claim,
  acknowledge the limitation instead of inventing information.
- The final piece should feel useful and actionable rather than being
  a simple transcript summary.

Grounding:
- The provided transcript material is the source of truth.
- Every substantive claim should be supported by the provided material.
- Do not mention this internal instruction or retrieval process.
""".strip()


def generate_ship_30_for_30_context(
    topic: str,
    top_k: int = 5,
) -> tuple[str, list[dict]]:
    """Retrieve transcript material for a Ship 30 for 30 article."""

    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    return build_retrieval_context(
        topic,
        top_k=top_k,
        max_words_per_source=700,
    )


def build_ship_30_for_30_prompt(
    topic: str,
    context: str,
) -> str:
    """Build the prompt used to generate a Ship 30 for 30 article."""

    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    if not context.strip():
        raise ValueError(
            "Transcript context is required to generate a grounded article."
        )

    return f"""
Write a Ship 30 for 30 style article about:

{topic}

Use only the transcript material below as factual source material.

{context}

Before finishing, make sure the article:
- is approximately 1,250 words
- has a strong opening hook
- has a clear narrative
- uses Markdown headings
- uses bullets where useful
- uses bold emphasis where useful
- contains concrete and practical takeaways
- remains grounded in the supplied transcripts
- does not invent unsupported claims or quotations
""".strip()


def build_ship_30_for_30_result(
    article: str,
    sources: list[dict],
) -> Ship30For30Result:
    """Create a structured result from a generated article."""

    if not article.strip():
        raise ValueError("Generated article cannot be empty.")

    return Ship30For30Result(
        article=article,
        sources=sources,
        word_count=len(article.split()),
    )