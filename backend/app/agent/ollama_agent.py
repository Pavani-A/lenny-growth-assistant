from collections.abc import Iterator

from app.agent.base import AgentResponse, GrowthAssistantAgent
from app.agent.config import AgentConfig
from app.agent.context import build_retrieval_context
from app.agent.skills.ship_30_for_30 import (
    SHIP_30_FOR_30_SYSTEM_PROMPT,
    SHIP_30_SECTIONS,
    build_ship_30_section_prompt,
    generate_ship_30_for_30_context,
)
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
        """Stream a grounded answer using conversation history and context."""

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

    def run_ship_30_for_30(
        self,
        topic: str,
    ) -> AgentResponse:
        """Generate a grounded approximately 1,250-word Ship 30 article."""

        if not topic.strip():
            raise ValueError("Topic cannot be empty.")

        print(
            "[Ship30] Retrieving transcript evidence...",
            flush=True,
        )

        context, sources = generate_ship_30_for_30_context(
            topic,
            top_k=2,
        )

        if not context:
            print(
                "[Ship30] No relevant transcript material found.",
                flush=True,
            )

            return AgentResponse(
                answer=(
                    "I couldn't find enough relevant material in the "
                    "Lenny transcript knowledge base to write this article."
                ),
                sources=[],
            )

        print(
            f"[Ship30] Retrieved {len(sources)} sources "
            f"with {len(context.split())} context words.",
            flush=True,
        )

        generated_sections: list[str] = []
        previous_text = ""
        current_word_count = 0

        total_sections = len(SHIP_30_SECTIONS)

        for index, section in enumerate(
            SHIP_30_SECTIONS,
            start=1,
        ):
            # Stop once the article reaches the minimum
            # acceptable length.
            if current_word_count >= 1100:
                print(
                    f"[Ship30] Minimum target reached: "
                    f"{current_word_count} words.",
                    flush=True,
                )
                break

            remaining_words = 1250 - current_word_count

            if remaining_words <= 0:
                print(
                    "[Ship30] Target word count reached.",
                    flush=True,
                )
                break

            # Use the section target, but reduce the requested
            # size when approaching the final target.
            target_words = min(
                section["target_words"],
                remaining_words,
            )

            # When only a small amount of content is needed,
            # request a short final section.
            if remaining_words <= 180:
                target_words = min(
                    target_words,
                    80,
                )

            print(
                f"[Ship30] Section {index}/{total_sections}: "
                f"{section['title']} "
                f"(target ~{target_words} words)...",
                flush=True,
            )

            prompt = build_ship_30_section_prompt(
                topic=topic,
                context=context,
                section_title=section["title"],
                section_goal=section["goal"],
                target_words=target_words,
                previous_text=previous_text,
            )

            try:
                section_text = self.provider.generate(
                    prompt,
                    system_prompt=SHIP_30_FOR_30_SYSTEM_PROMPT,
                )

            except Exception as exc:
                print(
                    f"[Ship30] Section {index} failed: {exc}",
                    flush=True,
                )
                raise

            if not section_text.strip():
                raise ValueError(
                    f"Ship 30 section '{section['title']}' "
                    "could not be generated."
                )

            section_text = section_text.strip()

            section_word_count = len(
                section_text.split()
            )

            generated_sections.append(section_text)

            # Pass only the latest section to the next generation.
            # The prompt builder itself limits this to the final
            # 40 words to keep the context small.
            previous_text = section_text

            current_word_count = len(
                " ".join(generated_sections).split()
            )

            print(
                f"[Ship30] Section {index} complete: "
                f"{section_word_count} words "
                f"(article total: {current_word_count})",
                flush=True,
            )

        article = "\n\n".join(
            generated_sections
        ).strip()

        if not article:
            raise ValueError(
                "The Ship 30 for 30 article could not be generated."
            )

        final_word_count = len(
            article.split()
        )

        print(
            f"[Ship30] Generation complete: "
            f"{final_word_count} words.",
            flush=True,
        )

        if final_word_count < 1100:
            raise ValueError(
                f"Ship 30 article is too short: "
                f"{final_word_count} words. "
                "Expected approximately 1,250 words."
            )

        if final_word_count > 1350:
            print(
                f"[Ship30] Warning: article is above the preferred "
                f"range ({final_word_count} words).",
                flush=True,
            )

        return AgentResponse(
            answer=article,
            sources=sources,
        )