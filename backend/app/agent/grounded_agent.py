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
7. Provide a sufficiently detailed answer when the transcript context
   supports it. Synthesize relevant information from multiple retrieved
   transcript sections when useful. Include explanations, examples,
   comparisons, or takeaways when they are supported by the transcripts.
8. When conversation history is provided, use it only to understand
   references and follow-up questions. Do not treat conversation
   history as evidence. Transcript context is the only source of truth.
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

    def _build_prompt(
        self,
        question: str,
        context: str,
        conversation_history: str = "",
    ) -> str:
        """Build the grounded prompt with optional conversation history."""

        if conversation_history.strip():
            history_section = f"""
PREVIOUS CONVERSATION:
{conversation_history}

Use the previous conversation ONLY to understand references,
follow-up questions, and what the user is referring to.

Do NOT treat previous assistant answers as factual evidence.
"""

        else:
            history_section = """
PREVIOUS CONVERSATION:
None
"""

        return f"""{SYSTEM_PROMPT}

{history_section}

RETRIEVED TRANSCRIPT CONTEXT:
{context}

CURRENT USER QUESTION:
{question}

Answer the CURRENT USER QUESTION.

Use the previous conversation only to understand what the user means.
Use ONLY the retrieved transcript context as factual evidence.

If the transcript context does not support a claim, do not present that
claim as a fact.
"""

    def answer(
        self,
        question: str,
        top_k: int = 5,
        conversation_history: str = "",
        retrieval_query: str | None = None,
    ) -> GroundedAgentResult:
        """Retrieve transcript context and generate a grounded answer."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        search_query = retrieval_query or question

        context, sources = build_grounded_context(
            search_query,
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

        prompt = self._build_prompt(
            question=question,
            context=context,
            conversation_history=conversation_history,
        )

        answer = self.agent.generate(prompt)

        return GroundedAgentResult(
            answer=answer,
            sources=sources,
        )

    def stream_answer(
        self,
        question: str,
        top_k: int = 5,
        conversation_history: str = "",
        retrieval_query: str | None = None,
    ):
        """Retrieve transcript context and stream a grounded answer."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        search_query = retrieval_query or question

        context, sources = build_grounded_context(
            search_query,
            top_k=top_k,
        )

        if not context:
            message = (
                "I couldn't find enough relevant material in the "
                "available Lenny Podcast transcripts to answer this."
            )

            def empty_context_stream():
                yield message

            return empty_context_stream(), []

        prompt = self._build_prompt(
            question=question,
            context=context,
            conversation_history=conversation_history,
        )

        stream = self.agent.generate_stream(prompt)

        return stream, sources