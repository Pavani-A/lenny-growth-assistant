
# Lenny Growth Assistant — Product Requirements Document

## 1. Product Overview

### Product Name

**The Lenny Growth Assistant**

### Product Summary

The Lenny Growth Assistant is an AI-powered conversational web application that helps product managers, founders, and growth professionals access knowledge from Lenny's Podcast transcripts.

Users can ask product and growth questions and receive answers grounded in the available transcript knowledge. The application also supports follow-up conversations, persistent conversation history, Ship 30 for 30-style content generation, Pi Coding Agent mode, and Markdown or HTML/CSS artifact generation.

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

- Prompt engineering
- Retrieval systems
- LLM providers
- Infrastructure
- Knowledge-base implementation

They should be able to ask a natural-language question and receive a useful, grounded response.

---

## 2.3 Problem Statement

Lenny's Podcast contains a large amount of product, growth, leadership, and startup knowledge.

However, this information is distributed across many episodes and transcripts. Finding the right discussion manually can be slow and difficult.

A general-purpose AI assistant also creates a trust problem because it may provide plausible answers that are not actually supported by Lenny's content.

The Lenny Growth Assistant addresses this by combining:

- Conversational interaction
- Transcript retrieval
- Grounded generation
- Source identification
- Session context
- Persistent conversation history

The product intentionally prioritizes grounded evidence over unrestricted general-purpose answers.

---

# 3. Product Goals

## Primary Goals

1. Make Lenny's Podcast knowledge easier to access.
2. Answer product and growth questions using transcript evidence.
3. Clearly identify supporting sources.
4. Preserve context across follow-up questions.
5. Avoid unsupported claims.
6. Provide a useful experience when the knowledge base cannot answer a question.
7. Generate reusable written content.
8. Generate and render useful artifacts inside the product.
9. Demonstrate an agent-based Growth Assistant using Pi Coding Agent.
10. Provide explicit LLM provider selection without changing application code.

---

# 4. Success Metrics

## 4.1 Grounded Answer Rate

### Target

**≥90%**

### Definition

Percentage of supported evaluation questions where the assistant produces an answer supported by relevant transcript evidence.

This metric is intended as an evaluation target for the system rather than a measured production statistic.

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
3. Receive a streamed answer.
4. View supporting source information.
5. Ask a follow-up question.
6. Receive a context-aware response.
7. View conversation history.
8. Ask an unsupported question.
9. Receive an appropriate insufficient-information response.
10. Generate a Ship 30 for 30-style article.
11. Generate an artifact.
12. View the artifact inside the application.
13. Enable Pi Agent mode and use the Growth Assistant flow.
14. Select different LLM providers and observe the corresponding provider behavior.

---

# 5. Assumptions

The following assumptions guided the implemented prototype.

## Content

- Lenny's Podcast/newsletter transcript content is available for the project.
- A curated transcript repository is sufficient for the initial implementation.
- The initial knowledge base does not need to contain every possible Lenny transcript to demonstrate the core experience.
- The current local knowledge base contains 50 podcast episodes.
- The current dataset contains 1,003 transcript chunks and 1,003 embeddings.

## Infrastructure

- PostgreSQL is used for application persistence.
- PostgreSQL runs locally through Docker Compose.
- pgvector is used for vector similarity search.
- The frontend and backend run as local development processes.
- Ollama runs locally for the demonstration.

## AI

- The application supports Anthropic Claude, OpenAI, and Ollama.
- Ollama provides the local model used for the demonstration.
- The chat model used by the local demo is `llama3.2:3b`.
- The embedding model used by the local demo is `embeddinggemma`.
- Embeddings are 768-dimensional.
- No model fine-tuning is required.
- Provider selection is handled through a provider abstraction and factory.
- The selected provider is used directly.
- There is no automatic fallback between providers.

## Agent

- Pi Coding Agent is used for the Growth Assistant agent path.
- Pi communicates with the application through its RPC interface.
- The current local Pi configuration uses Ollama and `llama3.2:3b`.
- Pi is currently executed without its built-in tools for the local small-model configuration.
- Transcript retrieval and factual grounding remain controlled by the application.

## Artifacts

- Generated HTML/CSS is considered untrusted content.
- HTML artifacts are rendered in a sandboxed iframe.
- Markdown and HTML/CSS artifacts are supported.

## Product

- The project is an evaluator-ready prototype rather than a production-scale SaaS product.
- Authentication and billing are not required for the current version.
- The focus is on grounded assistance, agent architecture, retrieval, provider flexibility, artifacts, and deployment readiness.

---

# 6. Scope

## 6.1 In Scope

### Conversational Assistant

- New chat sessions
- Independent session context
- Product and growth questions
- Follow-up questions
- Grounded answers
- Streaming responses
- Unsupported-question handling
- Persistent conversation history

### Knowledge Base

- Transcript ingestion
- Transcript cleaning and normalization
- Chunking
- Embedding generation
- Vector indexing
- Retrieval
- Source metadata
- Knowledge-base refresh process
- Source tracing

### AI / LLM

- Anthropic Claude
- OpenAI
- Ollama
- Explicit provider selection
- Provider abstraction
- Provider/model configuration
- Pi Coding Agent
- Local Ollama demonstration

### Content Generation

- Ship 30 for 30 capability
- Approximately 1,250-word articles
- Grounded claims
- Structured formatting
- Strong hooks
- Narrative structure
- Skimmable headings and sections
- Useful takeaways

### Artifacts

- Markdown generation
- HTML/CSS generation
- In-app Artifact Viewer
- HTML isolation through sandboxing

### Backend

- FastAPI
- PostgreSQL
- pgvector
- REST APIs
- Request validation
- Structured error responses
- Health endpoint
- Server-Sent Events streaming

### Operations

- Docker Compose for PostgreSQL
- Environment-based configuration
- `.env` / `.env.example` configuration pattern
- Application logging
- Error handling
- Automated tests
- Manual UI testing
- Documentation

---

## 6.2 Out of Scope

The following are intentionally excluded from the current version:

- General-purpose AI assistance
- Unrestricted web search
- General external research
- Foundation-model training
- Model fine-tuning
- Production billing
- Production-scale infrastructure
- Arbitrary code execution
- Native mobile applications
- Full enterprise authentication and authorization

### Why These Are Excluded

The assignment prioritizes a reliable, grounded assistant and evaluator-ready implementation.

Keeping the scope focused allows the project to demonstrate:

- Product judgment
- Grounding quality
- Agent architecture
- Retrieval
- Provider configuration
- Conversation persistence
- Artifact generation
- Deployment readiness

without spreading effort across unrelated production features.

---

# 7. Core User Flows

## 7.1 Start New Chat

### User Action

The user opens the application and starts a new conversation.

### System Behavior

The frontend creates a unique session ID for the conversation.

### Expected Result

The user receives an empty chat interface ready for a question.

The new session is independent from previously created conversations.

---

## 7.2 Ask a Grounded Question

### User Action

The user asks a product or growth question.

Example:

> "How can I improve user retention?"

### System Behavior

1. Receive the question.
2. Identify relevant transcript content.
3. Generate a query embedding.
4. Retrieve supporting transcript chunks using vector similarity.
5. Construct grounded context.
6. Generate an answer using the selected provider or agent path.
7. Stream the response to the frontend.
8. Return the supporting source information.
9. Persist the conversation.

### Expected Result

The user sees:

- Their question
- A grounded answer
- Supporting source information
- A progressively streamed response

---

## 7.3 Ask a Follow-Up Question

### User Action

The user asks a follow-up question based on the previous conversation.

### System Behavior

The system:

1. Retrieves the existing session.
2. Loads previous conversation messages.
3. Uses previous messages to understand conversational references.
4. Builds a retrieval query using recent user messages and the current question.
5. Retrieves new transcript evidence.
6. Generates a contextual response.
7. Persists the new message.

### Expected Result

The assistant understands the relationship between the current question and previous conversation context while continuing to use transcript evidence as the factual source of truth.

---

## 7.4 Unsupported Question

### User Action

The user asks something that cannot be sufficiently answered from the available transcripts.

### System Behavior

The system attempts transcript retrieval and evaluates the available context.

If useful transcript context is unavailable, the assistant does not invent an answer.

### Expected Result

The assistant explains that the available transcript material does not provide enough information.

---

## 7.5 Select an LLM Provider

### User Action

The user selects Ollama, Claude, or OpenAI from the provider selector.

### System Behavior

The application uses the explicitly selected provider.

There is no automatic fallback.

If Claude or OpenAI is selected without the required API configuration, the application returns a clear configuration error.

### Expected Result

The user receives a response from the selected provider or a clear provider-specific error.

---

## 7.6 Use Pi Agent Mode

### User Action

The user enables Pi Agent mode.

### System Behavior

1. The frontend switches the Growth Assistant flow to the Pi-based endpoint.
2. Pi Coding Agent is invoked.
3. Ollama is used as the local model provider.
4. Transcript retrieval provides the grounded context.
5. The response is streamed back to the frontend.
6. The normal provider selector is disabled while Pi mode is active.

### Expected Result

The user receives a grounded response through the Pi Coding Agent path.

---

## 7.7 Generate Ship 30 for 30 Article

### User Action

The user requests a Ship 30 for 30-style article based on grounded knowledge.

### System Behavior

The dedicated capability:

1. Uses relevant grounded information.
2. Applies the defined writing principles.
3. Produces approximately 1,250 words.
4. Uses structured formatting.
5. Keeps claims grounded in the available knowledge.

### Expected Result

The user receives reusable content containing:

- Strong hook
- Clear narrative
- Headings
- Skimmable sections
- Bullets where appropriate
- Selective bold emphasis
- Specific takeaway

---

## 7.8 Generate Artifact

### User Action

The user asks the assistant to create an artifact.

### Supported Outputs

- Markdown
- HTML/CSS

### Expected Result

The generated artifact appears in the Artifact Viewer beside the conversation.

The user does not need to copy generated HTML into another application just to inspect the result.

---

# 8. Functional Requirements

## FR-01 — Chat Sessions

The system shall allow users to start a new chat session.

Each session shall have an independent context.

---

## FR-02 — Conversation Persistence

The system shall persist:

- Session ID
- Messages
- Timestamps
- User metadata

in PostgreSQL.

---

## FR-03 — Transcript Retrieval

The system shall retrieve relevant transcript content before generating grounded answers.

The retrieval system shall use vector similarity search against transcript embeddings.

---

## FR-04 — Grounded Responses

The system shall use retrieved transcript evidence when answering supported product and growth questions.

The transcript context is the factual source of truth.

---

## FR-05 — Source Identification

Grounded responses shall provide relevant transcript source information.

Source information can include:

- Episode title
- Guest
- Published date
- Source URL
- YouTube URL
- Chunk index
- Transcript content

---

## FR-06 — Unsupported Questions

The system shall acknowledge when available transcript material does not sufficiently support the user's question.

It shall not present unsupported information as though it came from Lenny's transcripts.

---

## FR-07 — Follow-Up Context

The system shall preserve conversation context within a session.

Previous conversation messages may be used to understand references and follow-up questions.

Previous assistant responses shall not be treated as factual evidence.

---

## FR-08 — LLM Configuration

The system shall support:

- Anthropic Claude
- OpenAI
- Ollama

Provider/model selection shall be configurable without changing application code.

The selected provider shall be used directly without automatic fallback.

---

## FR-09 — Ollama Demonstration

The submitted demonstration shall run using Ollama and a suitable local model.

The current local configuration uses:

```text
Chat model: llama3.2:3b
Embedding model: embeddinggemma
Embedding dimension: 768
````

---

## FR-10 — Pi Coding Agent

The system shall provide a Pi Coding Agent execution path for the Growth Assistant.

The local demonstration shall use Pi with Ollama.

---

## FR-11 — Ship 30 for 30

The system shall provide a dedicated Ship 30 for 30 capability.

The generated content should be approximately 1,250 words and follow the required formatting and writing principles.

---

## FR-12 — Artifact Generation

The system shall generate Markdown or complete HTML/CSS artifacts when requested.

---

## FR-13 — Artifact Viewer

The frontend shall render generated artifacts beside the chat.

---

## FR-14 — Artifact Security

Generated HTML shall be treated as untrusted content and rendered using browser isolation through a sandboxed iframe.

---

## FR-15 — API Validation

Backend APIs shall validate incoming requests and return structured errors for invalid requests.

---

## FR-16 — Health Checks

The backend shall provide a health endpoint for basic application/service monitoring.

---

## FR-17 — Streaming

The system shall support streaming assistant responses using Server-Sent Events.

Streaming responses shall provide token/content events followed by source and completion events where applicable.

---

# 9. Non-Functional Requirements

## Reliability

The application should handle common failures gracefully, including:

* Missing API keys
* Unavailable Ollama
* Model failures/timeouts
* Empty retrieval results
* Database connection failures
* Invalid requests
* Artifact generation failures

Provider failures should not silently trigger a different provider.

---

## Performance

The system should provide reasonable response times for a local demonstration.

Retrieval should avoid sending the entire transcript corpus to the model.

The system retrieves a limited number of relevant transcript chunks for each query.

---

## Security

The application must:

* Keep secrets outside source control.
* Use environment variables for credentials.
* Provide an `.env.example` configuration pattern.
* Treat generated HTML as untrusted.
* Render generated HTML in a sandboxed iframe.
* Prevent generated artifacts from gaining unrestricted access to the host application.
* Avoid treating previous assistant responses as factual grounding evidence.

---

## Maintainability

The implementation should maintain clear separation between:

* Frontend
* API layer
* Agent layer
* Retrieval layer
* LLM providers
* Persistence
* Artifact generation
* Ingestion

This separation allows individual components to evolve without requiring changes throughout the application.

---

# 10. UI/UX Requirements

The application should provide a clean conversational experience.

## Main Chat

The initial state should allow the user to start a conversation easily.

## Grounded Answer

The interface should display the generated answer and make supporting transcript information easy to inspect.

## Not Enough Information

The interface should clearly communicate when available transcript material does not support the question.

## Artifact Viewer

Generated artifacts should be rendered beside the chat rather than shown only as raw code.

## Provider Visibility

The selected LLM provider should be visible in the interface.

When Pi Agent mode is active, the provider selector is disabled and Ollama is used for the local Pi flow.

## Responsive Behavior

The interface should remain usable across common desktop viewport sizes.

## Accessibility

The UI should provide:

* Readable typography
* Clear visual hierarchy
* Keyboard-accessible controls where applicable
* Meaningful labels
* Sufficient interaction feedback

---

# 11. Product States

The main product states are:

```text
Main Chat
    |
    v
User Question
    |
    v
Loading / Streaming
    |
    v
Grounded Answer
    |
    +---- Sources
    |
    +---- Follow-up Question
    |
    +---- Ship 30 for 30
    |
    +---- Artifact Generation
    |
    +---- Conversation History

OR

Not Enough Information

OR

Provider / Application Error
```

---

# 12. Current Implementation Snapshot

The current implementation provides:

```text
Knowledge Base
----------------
50 podcast episodes
1,003 transcript chunks
1,003 embeddings
768-dimensional vectors

Local AI
----------------
Ollama
llama3.2:3b
embeddinggemma

Agent
----------------
Pi Coding Agent
RPC execution
Local Ollama model

Persistence
----------------
PostgreSQL
pgvector
Conversation history
Session IDs

Frontend
----------------
React
Vite
Streaming chat
Provider selector
Pi Agent toggle
Source display
Artifact Viewer

Backend
----------------
FastAPI
REST APIs
SSE streaming
Pydantic validation
Application logging
```

The backend automated test suite currently passes with:

```text
23 passed
```

The implementation therefore covers the primary product, grounding, agent, persistence, artifact, provider, and UI requirements of the prototype.


