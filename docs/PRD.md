# Lenny Growth Assistant — Product Requirements Document

## 1. Product Overview

### Product Name

**The Lenny Growth Assistant**

### Product Summary

The Lenny Growth Assistant is an AI-powered conversational web application that helps product managers, founders, and growth professionals access knowledge from Lenny's Podcast transcripts.

Users can ask product and growth questions and receive answers grounded in the available transcript knowledge. The application also supports follow-up conversations, Ship 30 for 30-style content generation, and Markdown or HTML/CSS artifact generation.

The core product principle is:

> **Grounded usefulness over confident guessing.**

The assistant should clearly acknowledge when the available transcript material does not support an answer rather than inventing information.

---

# 2. User & Problem

## 2.1 Primary Users

### Product Managers

Product managers can use the assistant to explore product strategy, user research, prioritization, retention, growth, and other product-related topics.

### Founders and Startup Teams

Founders can use the assistant to quickly explore startup and growth lessons contained in Lenny's Podcast.

### Growth Professionals

Growth professionals can use the assistant to find relevant ideas and approaches from conversations with experienced product and growth leaders.

---

## 2.2 User Job

The primary user job is:

> "Help me quickly find and apply relevant product or growth knowledge from Lenny's Podcast without manually searching through many transcripts."

Users should not need to understand:

- Prompt engineering.
- Retrieval systems.
- LLM providers.
- Infrastructure.
- Knowledge-base implementation.

They should be able to ask a natural-language question and receive a useful, grounded response.

---

## 2.3 Problem Statement

Lenny's Podcast contains a large amount of product, growth, leadership, and startup knowledge.

However, this information is distributed across many episodes and transcripts. Finding the right discussion manually can be slow and difficult.

A general-purpose AI assistant also creates a trust problem because it may provide plausible answers that are not actually supported by Lenny's content.

The Lenny Growth Assistant addresses this by combining:

- Conversational interaction.
- Transcript retrieval.
- Grounded generation.
- Source identification.
- Session context.

---

# 3. Product Goals

## Primary Goals

1. Make Lenny's Podcast knowledge easier to access.
2. Answer product and growth questions using transcript evidence.
3. Clearly identify supporting sources.
4. Preserve context across follow-up questions.
5. Avoid unsupported claims.
6. Provide a useful experience even when the knowledge base cannot answer a question.
7. Generate reusable written content.
8. Generate and render useful artifacts inside the product.

---

# 4. Success Metrics

## 4.1 Grounded Answer Rate

### Target

**≥90%**

### Definition

Percentage of supported evaluation questions where the assistant produces an answer that is supported by relevant transcript evidence.

This measures whether the retrieval and grounding system is producing useful answers rather than merely generating plausible responses.

---

## 4.2 Unsupported Question Safety Rate

### Target

**100%**

### Definition

Percentage of deliberately unsupported questions where the assistant correctly acknowledges that the available transcript material does not provide enough information.

The assistant should not fabricate a Lenny-sourced answer when supporting evidence is unavailable.

---

## 4.3 Core Flow Completion

The evaluator should be able to complete the major product flows successfully:

1. Start a new chat.
2. Ask a grounded question.
3. Receive an answer.
4. View the supporting source.
5. Ask a follow-up question.
6. Receive a context-aware response.
7. Ask an unsupported question.
8. Receive an appropriate "not enough information" response.
9. Generate a Ship 30 for 30-style article.
10. Generate an artifact.
11. View the artifact inside the application.

---

# 5. Assumptions

The assignment leaves some implementation details open. The following assumptions will guide the project.

## Content

- Lenny's Podcast/newsletter transcript content is available for the project.
- A curated transcript repository is sufficient for the initial implementation.
- The knowledge base does not need to contain every possible Lenny transcript to demonstrate the core experience.

## Infrastructure

- PostgreSQL will be used for application persistence.
- Local PostgreSQL will run through Docker Compose.
- Supabase and Railway can be used as alternative PostgreSQL deployments if required.

## AI

- The application will support Anthropic Claude and OpenAI as cloud providers.
- Ollama will provide the mandatory local model for the demonstration.
- No model fine-tuning is required.
- The application will use a configuration layer so the model/provider can be changed without modifying application code.

## Artifacts

- Generated HTML/CSS is considered untrusted content.
- The Artifact Viewer will therefore use an appropriate isolation and/or sanitization strategy.

## Product

- The project is an evaluator-ready prototype rather than a production-scale SaaS product.
- Authentication and billing are not required for the initial version.

---

# 6. Scope

## 6.1 In Scope

### Conversational Assistant

- New chat sessions.
- Independent session context.
- Product and growth questions.
- Follow-up questions.
- Grounded answers.
- Unsupported-question handling.

### Knowledge Base

- Transcript ingestion.
- Transcript cleaning and normalization.
- Chunking.
- Indexing.
- Retrieval.
- Source metadata.
- Knowledge-base refresh process.
- Source tracing.

### AI

- Anthropic Claude.
- OpenAI.
- Ollama.
- Anthropic Claude Agent SDK.
- Configuration-based provider selection.

### Content Generation

- Ship 30 for 30 skill/tool.
- Approximately 1,250-word articles.
- Grounded claims.
- Structured formatting.

### Artifacts

- Markdown generation.
- HTML/CSS generation.
- In-app Artifact Viewer.
- Artifact security/isolation.

### Backend

- FastAPI.
- PostgreSQL.
- REST APIs.
- Request validation.
- Structured errors.
- Health endpoints.

### Operations

- Docker Compose.
- `.env.example`.
- Structured logging.
- Error handling.
- Automated tests.
- Manual UI test plan.
- Documentation.

---

## 6.2 Out of Scope

The following are intentionally excluded from the initial version:

- General-purpose AI assistance.
- Unrestricted web search.
- General external research.
- Foundation-model training.
- Model fine-tuning.
- Production billing.
- Production-scale infrastructure.
- Arbitrary code execution.
- Native mobile applications.
- Full enterprise authentication and authorization.

### Why These Are Excluded

The assignment prioritizes a reliable, grounded assistant and evaluator-ready deployment.

Keeping the scope focused allows the project to demonstrate:

- Product judgment.
- Grounding quality.
- Agent architecture.
- Retrieval.
- Provider configuration.
- Artifact generation.
- Deployment readiness.

without spreading effort across unrelated production features.

---

# 7. Core User Flows

## 7.1 Start New Chat

### User Action

The user opens the application and starts a new conversation.

### System Behavior

The system creates a unique session.

### Expected Result

The user receives an empty chat interface ready for a question.

---

## 7.2 Ask a Grounded Question

### User Action

The user asks a product or growth question.

Example:

> "How can I improve user retention?"

### System Behavior

1. Receive the question.
2. Identify relevant transcript content.
3. Retrieve supporting transcript chunks.
4. Evaluate whether enough evidence exists.
5. Generate an answer grounded in the retrieved content.
6. Identify the supporting source.
7. Persist the conversation.

### Expected Result

The user sees:

- Their question.
- A grounded answer.
- A grounding indicator.
- Supporting source information.

---

## 7.3 Ask a Follow-Up Question

### User Action

The user asks a follow-up question based on the previous conversation.

### System Behavior

The system:

1. Retrieves the existing session.
2. Uses conversation context.
3. Retrieves relevant transcript evidence.
4. Generates a contextual answer.
5. Persists the new message.

### Expected Result

The assistant understands the relationship between the current question and previous conversation context.

---

## 7.4 Unsupported Question

### User Action

The user asks something that cannot be sufficiently answered from the available transcripts.

### System Behavior

The system determines that relevant supporting evidence is insufficient.

### Expected Result

Instead of generating an unsupported answer, the assistant explains that the available transcript material does not provide enough information.

The UI can optionally provide suggested supported topics.

---

## 7.5 Generate Ship 30 for 30 Article

### User Action

The user requests a Ship 30 for 30-style article based on the current conversation or grounded knowledge.

### System Behavior

The dedicated Ship 30 for 30 skill:

1. Uses grounded information.
2. Applies the defined writing principles.
3. Produces approximately 1,250 words.
4. Uses structured formatting.
5. Keeps claims grounded in the knowledge base.

### Expected Result

The user receives a reusable article with:

- Strong hook.
- Clear narrative.
- Headings.
- Bullets where appropriate.
- Selective bold emphasis.
- Specific takeaway.

---

## 7.6 Generate Artifact

### User Action

The user asks the assistant to create an artifact.

### Supported Outputs

- Markdown.
- HTML/CSS.

### Expected Result

The generated artifact appears in the Artifact Viewer beside the conversation.

The user should not need to copy the generated code into another application just to see the result.

---

# 8. Functional Requirements

## FR-01 — Chat Sessions

The system shall allow users to start a new chat session.

Each session shall have an independent context.

---

## FR-02 — Conversation Persistence

The system shall persist:

- Session ID.
- Messages.
- Timestamps.
- User metadata.

in PostgreSQL.

---

## FR-03 — Transcript Retrieval

The system shall retrieve relevant transcript content before generating grounded answers.

---

## FR-04 — Grounded Responses

The system shall use retrieved transcript evidence when answering supported product and growth questions.

---

## FR-05 — Source Identification

Grounded answers shall clearly identify the relevant transcript/source used.

---

## FR-06 — Unsupported Questions

The system shall acknowledge when available transcript material does not sufficiently support the user's question.

It shall not present unsupported information as though it came from Lenny's transcripts.

---

## FR-07 — Follow-Up Context

The system shall preserve conversation context within a session.

---

## FR-08 — LLM Configuration

The system shall support:

- Anthropic Claude.
- OpenAI.
- Ollama.

Provider/model selection shall be configurable without changing application code.

---

## FR-09 — Ollama Demonstration

The submitted demonstration shall run using Ollama and a suitable local model.

---

## FR-10 — Ship 30 for 30

The system shall provide a dedicated Ship 30 for 30 skill/tool.

The generated content should be approximately 1,250 words and follow the required formatting and writing principles.

---

## FR-11 — Artifact Generation

The system shall generate Markdown or complete HTML/CSS artifacts when requested.

---

## FR-12 — Artifact Viewer

The frontend shall render generated artifacts beside the chat.

---

## FR-13 — Artifact Security

Generated HTML shall be treated as untrusted content and rendered using an appropriate isolation and/or sanitization strategy.

---

## FR-14 — API Validation

Backend APIs shall validate incoming requests and return structured errors for invalid requests.

---

## FR-15 — Health Checks

The backend shall provide health endpoints for application/service monitoring.

---

# 9. Non-Functional Requirements

## Reliability

The application should handle common failures gracefully, including:

- Missing API keys.
- Unavailable Ollama.
- Model timeouts.
- Empty retrieval results.
- Database connection failures.

---

## Performance

The system should provide reasonable response times for a local demonstration.

Retrieval should avoid unnecessarily sending the entire transcript corpus to the model.

---

## Security

The application must:

- Keep secrets outside source control.
- Use environment variables for credentials.
- Provide `.env.example`.
- Treat generated HTML as untrusted.
- Prevent artifacts from gaining unsafe access to the host application.

---

## Maintainability

The implementation should have clear separation between:

- Frontend.
- API layer.
- Agent layer.
- Retrieval layer.
- LLM providers.
- Persistence.
- Artifact generation.

---

# 10. UI/UX Requirements

The application should provide a clean conversational experience.

## Main Chat

The initial state should allow the user to start a conversation easily.

## Grounded Answer

The interface should make it clear that the answer is grounded and show the supporting source.

## Not Enough Information

The interface should clearly communicate that available transcript material does not support the question.

## Artifact Viewer

Generated artifacts should be rendered beside the chat rather than shown only as raw code.

## Provider Visibility

The selected LLM provider/model should be visible in the UI or configuration.

## Responsive Behavior

The interface should remain usable across common desktop viewport sizes.

## Accessibility

The UI should provide:

- Readable typography.
- Clear visual hierarchy.
- Keyboard-accessible controls.
- Meaningful labels.
- Sufficient interaction feedback.

---

# 11. Product States

The main product states are:

```text
Main Chat
    ↓
User Question
    ↓
Loading
    ↓
Grounded Answer
    │
    ├── Follow-up Question
    │
    ├── Ship 30 for 30
    │
    └── Artifact Generation

OR

Not Enough Information

OR

Error