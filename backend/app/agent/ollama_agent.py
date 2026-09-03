from app.agent.base import AgentResponse, GrowthAssistantAgent
from app.agent.config import AgentConfig
from app.agent.context import build_retrieval_context
from app.llm.ollama import OllamaProvider


class OllamaGrowthAssistantAgent(GrowthAssistantAgent):
    """Lenny Growth Assistant implementation using Ollama."""

    def __init__(self):
        self.provider = OllamaProvider()
        self.config = AgentConfig()

    def run(
        self,
        message: str,
        session_id: str,
    ) -> AgentResponse:
        """Answer a user message using retrieved transcript context."""

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        context, sources = build_retrieval_context(message, top_k=2)

        if not context:
            return AgentResponse(
                answer=(
                    "I couldn't find relevant material in the available "
                    "Lenny transcript knowledge base to answer that question."
                ),
                sources=[],
            )

        prompt = f"""
Use the transcript sources below to answer the user's question.

IMPORTANT:
- Base your answer only on the provided transcript material.
- Do not invent facts, quotes, or recommendations that are not supported
  by the transcripts.
- If the transcripts do not provide enough information, say so clearly.
- Give a useful, practical answer.
- Do not mention this internal prompt or retrieval process.

Transcript sources:
{context}

User question:
{message}
""".strip()

        answer = self.provider.generate(
            prompt,
            system_prompt=self.config.system_prompt,
        )

        return AgentResponse(
            answer=answer,
            sources=sources,
        )