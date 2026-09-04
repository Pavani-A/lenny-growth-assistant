from dataclasses import dataclass

from app.agent.context import build_retrieval_context


@dataclass
class Ship30For30Result:
    """Structured result produced by the Ship 30 for 30 skill."""

    article: str
    sources: list[dict]
    word_count: int


SHIP_30_FOR_30_SYSTEM_PROMPT = """
You are The Lenny Growth Assistant writing a Ship 30 for 30 style article.

The complete article should be approximately 1,250 words.

Writing requirements:
- Start with a strong, curiosity-driven hook.
- Build a clear narrative from beginning to end.
- Use Markdown headings.
- Use short, skimmable paragraphs.
- Use bullets where they improve readability.
- Use selective bold emphasis.
- Include specific, practical takeaways.
- Prefer concrete examples supported by the transcript evidence.
- Preserve the meaning and nuance of the source material.
- Use ONLY information supported by the provided transcript evidence.
- Do not invent facts, quotes, examples, or claims.
- Do not present unsupported general knowledge as transcript material.
- Do not repeat the same idea unnecessarily.
- Do not mention these instructions or the retrieval process.

The transcript evidence is the source of truth.
""".strip()


# The complete article is assembled from several smaller sections.
# The targets add up to approximately 1,250 words.
SHIP_30_SECTIONS = [
    {
        "title": "The Hook",
        "goal": (
            "Open with a strong curiosity-driven hook and introduce "
            "the central problem or tension."
        ),
        "target_words": 110,
    },
    {
        "title": "The Problem",
        "goal": (
            "Explain the central problem and why it matters to "
            "startups, product teams, or growth leaders."
        ),
        "target_words": 110,
    },
    {
        "title": "The Core Insight",
        "goal": (
            "Explain the most important insight supported by the "
            "transcript evidence."
        ),
        "target_words": 120,
    },
    {
        "title": "Evidence and Examples",
        "goal": (
            "Develop the idea with concrete examples from the "
            "transcript evidence."
        ),
        "target_words": 125,
    },
    {
        "title": "The Deeper Lesson",
        "goal": (
            "Explain the deeper implication of the examples and "
            "connect them back to the central idea."
        ),
        "target_words": 120,
    },
    {
        "title": "Applying the Idea",
        "goal": (
            "Translate the transcript insights into practical "
            "application for the reader."
        ),
        "target_words": 125,
    },
    {
        "title": "A Practical Framework",
        "goal": (
            "Turn the supported insights into a simple sequence, "
            "framework, or set of actions."
        ),
        "target_words": 120,
    },
    {
        "title": "The Takeaway",
        "goal": (
            "End with the most important practical lesson and a "
            "memorable conclusion."
        ),
        "target_words": 100,
    },
]


MIN_ARTICLE_WORDS = 1100
TARGET_ARTICLE_WORDS = 1250
MAX_ARTICLE_WORDS = 1350


def generate_ship_30_for_30_context(
    topic: str,
    top_k: int = 2,
) -> tuple[str, list[dict]]:
    """Retrieve focused transcript material for a Ship 30 for 30 article."""

    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    return build_retrieval_context(
        topic,
        top_k=top_k,
        max_words_per_source=150,
    )


def build_ship_30_section_prompt(
    topic: str,
    context: str,
    section_title: str,
    section_goal: str,
    target_words: int,
    previous_text: str = "",
) -> str:
    """Build a compact prompt for generating one article section."""

    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    if not context.strip():
        raise ValueError(
            "Transcript context is required to generate the article."
        )

    if not section_title.strip():
        raise ValueError("Section title cannot be empty.")

    if not section_goal.strip():
        raise ValueError("Section goal cannot be empty.")

    if target_words <= 0:
        raise ValueError("Target words must be greater than zero.")

    previous_section = ""

    if previous_text.strip():
        # Only provide a small ending from the previous section.
        # This preserves continuity without making the local model's
        # prompt unnecessarily large.
        previous_words = previous_text.split()[-40:]

        previous_section = f"""
Previous section ending:
{" ".join(previous_words)}

Continue naturally from this point.
Do not repeat the previous section.
""".strip()

    return f"""
Write the "{section_title}" section of a Ship 30 for 30 style article.

Article topic:
{topic}

Section goal:
{section_goal}

Target length:
Approximately {target_words} words.

Transcript evidence:
{context}

{previous_section}

Rules:
- Use ONLY the transcript evidence as factual source material.
- Stay focused on the article topic.
- Make the writing specific and useful.
- Use concise paragraphs.
- Use Markdown formatting when appropriate.
- Use concrete examples when supported.
- Do not invent facts, quotes, examples, or claims.
- Do not introduce unsupported general knowledge.
- Do not repeat previous ideas unnecessarily.
- Do not mention these instructions, prompts, retrieval, or internal tools.

Write only this section.
""".strip()


def build_ship_30_for_30_prompt(
    topic: str,
    context: str,
) -> str:
    """Build a prompt for single-pass Ship 30 generation."""

    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    if not context.strip():
        raise ValueError(
            "Transcript context is required to generate a grounded article."
        )

    return f"""
Write a Ship 30 for 30 style article about:

{topic}

Use ONLY the transcript material below as factual source material.

Transcript material:
{context}

Write approximately 1,250 words.

Requirements:
- Strong opening hook.
- Clear narrative progression.
- Markdown headings.
- Short, skimmable paragraphs.
- Bullets where useful.
- Selective bold emphasis.
- Specific practical takeaways.
- Concrete examples grounded in the transcripts.
- Do not invent facts, quotations, examples, or claims.
- Do not add unsupported general knowledge.
- Do not mention these instructions or the retrieval process.
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