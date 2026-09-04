from dataclasses import dataclass

from app.agent.pi_agent import PiAgent
from app.retrieval.context import build_grounded_context


SYSTEM_PROMPT = """You are The Lenny Growth Assistant.

Your job is to answer product and growth questions using ONLY the
provided Lenny Podcast transcript context.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts, quotes, examples, or recommendations.
3. Ground important claims in the provided transcript context.
4. When useful, mention the relevant guest or episode.
5. If the provided context does not contain enough information to
   answer the question, clearly say that the available Lenny Podcast
   material does not provide enough evidence.
6. Give a useful, clear answer rather than simply repeating the
   transcripts.

Retrieved transcript context:
"""


@dataclass
class GroundedAgentResult:
    """Result returned by the grounded Lenny agent."""

    answer: str
    sources: list[dict]


class GroundedLennyAgent:
    """Generate Lenny-grounded answers through Pi Coding Agent."""

    def __init__(
        self,
        provider: str = "ollama",
        model: str = "llama3.2:3b",
    ):
        self.agent = PiAgent(
            provider=provider,
            model=model,
        )

    def answer(
        self,
        question: str,
        top_k: int = 5,
    ) -> GroundedAgentResult:
        """Retrieve transcript context and generate a grounded answer."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        context, sources = build_grounded_context(
            question,
            top_k=top_k,
        )

        if not context:
            return GroundedAgentResult(
                answer=(
                    "I couldn't find enough relevant material in the "
                    "available Lenny Podcast transcripts to answer this."
                ),
                sources=[],
            )

        prompt = f"""{SYSTEM_PROMPT}

{context}

USER QUESTION:
{question}

Answer the user's question using only the transcript context above.
"""

        answer = self.agent.generate(prompt)

        return GroundedAgentResult(
            answer=answer,
            sources=sources,
        )