from collections.abc import Iterator

from app.agent.base import AgentResponse, GrowthAssistantAgent
from app.agent.config import AgentConfig
from app.agent.context import build_retrieval_context
from app.llm.ollama import OllamaProvider


class OllamaGrowthAssistantAgent(GrowthAssistantAgent):
    """Lenny Growth Assistant implementation using Ollama."""

    def __init__(self):
        self.provider = OllamaProvider()
        self.config = AgentConfig()

    def _build_prompt(
        self,
        message: str,
        context: str,
        conversation_history: str = "",
    ) -> str:
        """Build the grounded prompt with optional conversation history."""

        history_section = ""

        if conversation_history.strip():
            history_section = f"""
Previous conversation:
{conversation_history}

Use the previous conversation only to understand the user's
follow-up questions and context. Ground factual answers in the
provided transcript sources.
""".strip()

        return f"""
Use the transcript sources below to answer the user's question.

IMPORTANT:
- Base factual claims and recommendations only on the provided transcript material.
- Do not invent facts, quotes, or recommendations that are not supported
  by the transcripts.
- Use the previous conversation to understand follow-up questions.
- If the transcripts do not provide enough information, say so clearly.
- Give a useful, practical answer.
- Do not mention this internal prompt or retrieval process.

{history_section}

Transcript sources:
{context}

User question:
{message}
""".strip()

    def run(
        self,
        message: str,
        session_id: str,
        conversation_history: str = "",
    ) -> AgentResponse:
        """Answer a user message using conversation history and RAG context."""

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        context, sources = build_retrieval_context(
            message,
            top_k=2,
        )

        if not context:
            return AgentResponse(
                answer=(
                    "I couldn't find relevant material in the available "
                    "Lenny transcript knowledge base to answer that question."
                ),
                sources=[],
            )

        prompt = self._build_prompt(
            message=message,
            context=context,
            conversation_history=conversation_history,
        )

        answer = self.provider.generate(
            prompt,
            system_prompt=self.config.system_prompt,
        )

        return AgentResponse(
            answer=answer,
            sources=sources,
        )

    def run_stream(
        self,
        message: str,
        session_id: str,
        conversation_history: str = "",
    ) -> tuple[Iterator[str], list[dict]]:
        """Stream a grounded answer using conversation history and RAG context."""

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        context, sources = build_retrieval_context(
            message,
            top_k=2,
        )

        if not context:

            def no_results() -> Iterator[str]:
                yield (
                    "I couldn't find relevant material in the available "
                    "Lenny transcript knowledge base to answer that question."
                )

            return no_results(), []

        prompt = self._build_prompt(
            message=message,
            context=context,
            conversation_history=conversation_history,
        )

        stream = self.provider.generate_stream(
            prompt,
            system_prompt=self.config.system_prompt,
        )

        return stream, sources