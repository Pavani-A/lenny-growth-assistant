import json
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

            target_words = min(
                section["target_words"],
                remaining_words,
            )

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

    def run_artifact(
        self,
        prompt: str,
        session_id: str,
    ) -> dict:
        """Generate a structured HTML or Markdown artifact."""

        if not prompt.strip():
            raise ValueError("Artifact prompt cannot be empty.")

        if not session_id.strip():
            raise ValueError("Session ID cannot be empty.")

        print(
            "[Artifact] Retrieving transcript evidence...",
            flush=True,
        )

        context, sources = build_retrieval_context(
            prompt,
            top_k=2,
            max_words_per_source=150,
        )

        print(
            f"[Artifact] Retrieved {len(sources)} sources.",
            flush=True,
        )

        artifact_system_prompt = """
You are the artifact-generation component of The Lenny Growth Assistant.

Create a polished artifact based ONLY on the supplied Lenny's Podcast
transcript evidence.

DO NOT return JSON.
DO NOT return Markdown code fences.
DO NOT explain what you are doing.

Return exactly this structure:

TITLE:
A short descriptive title

TYPE:
html

CONTENT:
<artifact content>

Rules:
- TYPE must be exactly html or markdown.
- Prefer html for visual artifacts such as dashboards, checklists,
  frameworks, comparisons, and growth experiment plans.
- For HTML, create useful, clean HTML.
- Put CSS inside a <style> tag.
- Do not use <script> tags.
- Do not use iframes.
- Do not use external stylesheets.
- Do not use external JavaScript.
- Do not use external images.
- Do not use remote resources.
- Do not make network requests.
- Keep the artifact safe for an isolated viewer.
- Use only claims supported by the supplied transcript evidence.
- Do not invent statistics, quotes, examples, or facts.
- Make the artifact practical and visually structured.
- Use headings, cards, tables, checklists, and lists where appropriate.
- Keep the artifact reasonably concise.
- Do not add unnecessary explanations outside the artifact.
""".strip()

        prompt_text = f"""
Create an artifact for this user request:

{prompt}

Relevant transcript evidence:

{context if context else "No relevant transcript evidence was found."}

The artifact must be grounded in the supplied transcript evidence.

If the transcript evidence does not support an important claim,
make that limitation clear inside the artifact instead of inventing information.

Return:

TITLE:
...

TYPE:
html

CONTENT:
...

Do not include END_ARTIFACT.
The response may end immediately after the artifact content.
""".strip()

        try:
            response = self.provider.generate(
                prompt_text,
                system_prompt=artifact_system_prompt,
            )

        except Exception as exc:
            raise RuntimeError(
                f"Artifact generation failed: {exc}"
            ) from exc

        response = response.strip()

        print(
            "[Artifact] Raw model response received.",
            flush=True,
        )
        print(response, flush=True)

        title_marker = "TITLE:"
        type_marker = "TYPE:"
        content_marker = "CONTENT:"

        type_start = response.find(type_marker)

        if type_start == -1:
            print(
                "[Artifact] Model did not provide TYPE:",
                flush=True,
            )
            print(response, flush=True)

            raise RuntimeError(
                "The model returned an invalid artifact format."
            )

        # Everything before TYPE is treated as the title section.
        title_section = response[:type_start].strip()

        if title_section.startswith(title_marker):
            title = title_section[
                len(title_marker):
            ].strip()
        else:
            # Small local models may omit TITLE:.
            title_lines = [
                line.strip()
                for line in title_section.splitlines()
                if line.strip()
            ]

            title = title_lines[0] if title_lines else ""

        # Find the start of the actual artifact content.
        content_start = response.find(
            content_marker,
            type_start + len(type_marker),
        )

        if content_start != -1:
            # Normal case:
            #
            # TYPE:
            # html
            #
            # CONTENT:
            # <html>
            type_section = response[
                type_start + len(type_marker):content_start
            ].strip()

            artifact_type = type_section.lower()

            content = response[
                content_start + len(content_marker):
            ].strip()

        else:
            # Local models may omit CONTENT:.
            #
            # In that case, the first line after TYPE: is
            # treated as the artifact type and everything after
            # that line becomes the artifact content.
            type_line_end = response.find(
                "\n",
                type_start + len(type_marker),
            )

            if type_line_end == -1:
                artifact_type = response[
                    type_start + len(type_marker):
                ].strip().lower()

                content = ""

            else:
                artifact_type = response[
                    type_start + len(type_marker):type_line_end
                ].strip().lower()

                content = response[
                    type_line_end:
                ].strip()

        # Remove accidental Markdown fences if the model adds them.
        if content.startswith("```"):
            lines = content.splitlines()

            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            content = "\n".join(lines).strip()

        if artifact_type not in {"html", "markdown"}:
            raise RuntimeError(
                "Artifact type must be 'html' or 'markdown'."
            )

        if not title:
            raise RuntimeError(
                "Artifact title is missing or invalid."
            )

        if not content:
            raise RuntimeError(
                "Artifact content is missing or invalid."
            )

        # If the model produced an HTML fragment instead of a
        # complete document, wrap it in a safe self-contained document.
        if artifact_type == "html":
            lowered_content = content.lower()

            if (
                "<!doctype html" not in lowered_content
                and "<html" not in lowered_content
            ):
                content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
{content}
</body>
</html>"""

        print(
            f"[Artifact] Generated '{title}' "
            f"({artifact_type}).",
            flush=True,
        )

        return {
            "type": artifact_type,
            "title": title,
            "content": content,
            "sources": sources,
        }