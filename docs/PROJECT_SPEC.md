# Lenny Growth Assistant — Project Specification

## 1. Product Overview

### Product Name

**The Lenny Growth Assistant**

### Product Description

The Lenny Growth Assistant is a full-stack AI conversational application that helps users answer product and growth questions using knowledge grounded in Lenny's Podcast transcripts.

Users can:

* Ask product and growth questions.
* Receive answers grounded in transcript content.
* View supporting sources.
* Continue conversations with preserved context.
* View persistent conversation history.
* Generate Ship 30 for 30-style content.
* Generate Markdown or HTML/CSS artifacts.
* View generated artifacts inside the application.
* Select between supported LLM providers.
* Use the Pi Coding Agent Growth Assistant flow.

### Core Product Principle

> **Grounded usefulness over confident guessing.**

If the available transcript material does not support an answer, the assistant should clearly say that it does not have enough information rather than inventing an answer.

---

# 2. Users & Problem

## Primary Users

* Product Managers
* Founders and startup teams
* Growth professionals

## User Problem

Lenny's Podcast contains a large amount of product, growth, leadership, and startup knowledge.

Finding relevant information manually across transcripts can be time-consuming. A general-purpose AI assistant may also provide answers that are not supported by Lenny's content.

## Solution

The Lenny Growth Assistant provides a conversational interface over the transcript knowledge base so users can ask questions naturally and receive grounded answers with supporting source information.

The application combines:

* Transcript ingestion
* Vector retrieval
* Grounded generation
* Source tracing
* Persistent conversations
* Multiple LLM providers
* Pi Coding Agent integration
* Artifact generation

---

# 3. Discovery Brief

## Success Metrics

### Grounded Answer Rate

Target: **≥90%**

Measure the percentage of supported questions that receive answers grounded in relevant transcript evidence.

This is an evaluation target for the prototype rather than a measured production metric.

### Unsupported Question Safety Rate

Target: **100%**

For deliberately unsupported questions, the assistant should avoid presenting unsupported information as though it came from Lenny's content.

### Core Flow Completion

The evaluator should be able to successfully complete the main product flows:

* Start a chat.
* Ask a grounded question.
* Receive a streamed answer.
* View supporting sources.
* Ask a follow-up question.
* Continue the conversation using preserved context.
* View previous conversations.
* Ask an unsupported question.
* Generate a Ship 30 for 30 article.
* Generate an artifact.
* View the artifact.
* Enable Pi Agent mode.
* Select an LLM provider.

## Assumptions

* Lenny Podcast/newsletter transcript content is available for the project.
* A curated transcript repository is sufficient for the initial implementation.
* PostgreSQL will be used for persistence.
* PostgreSQL will run locally through Docker Compose.
* pgvector will be used for vector similarity search.
* Ollama will be available for the local demonstration.
* Cloud LLM providers can be configured through environment variables when required.
* No model fine-tuning is required.
* Generated HTML/CSS will be treated as untrusted content.
* The project is an evaluator-ready prototype rather than production-scale SaaS.

## Scope

### In Scope

* Grounded conversational assistant.
* Independent chat sessions.
* Persistent conversations.
* PostgreSQL persistence.
* Transcript ingestion and retrieval.
* Vector similarity search.
* Source tracing.
* Follow-up conversation context.
* Anthropic Claude support.
* OpenAI support.
* Ollama support.
* Explicit LLM provider selection.
* Pi Coding Agent.
* Ship 30 for 30 capability.
* Markdown artifacts.
* HTML/CSS artifacts.
* In-app Artifact Viewer.
* API validation.
* Structured errors.
* Health endpoint.
* Server-Sent Events streaming.
* Application logging.
* Automated tests.
* Docker Compose database setup.
* Documentation.

### Out of Scope

* General-purpose AI assistant.
* Unrestricted web search.
* General external research.
* Foundation-model training.
* Model fine-tuning.
* Production-scale SaaS infrastructure.
* Production billing.
* Arbitrary code execution.
* Native mobile applications.
* Full enterprise authentication and authorization.

## Key Risks

* Hallucination.
* Poor transcript retrieval.
* Local model quality.
* Model latency.
* Cloud API cost.
* Ollama unavailable.
* Database failures.
* Stale transcript data.
* Unsafe HTML rendering.
* Incorrect provider configuration.

---

# 4. Goals & Non-Goals

## Product Goals

1. Make Lenny's Podcast knowledge easier to access.
2. Provide trustworthy, transcript-grounded answers.
3. Show supporting sources.
4. Preserve conversation context.
5. Clearly handle unsupported questions.
6. Support cloud and local LLM providers.
7. Generate Ship 30 for 30-style content.
8. Generate and display artifacts.
9. Demonstrate an agent-based Growth Assistant using Pi Coding Agent.
10. Provide a reproducible and testable project.

## Technical Goals

* React + Vite frontend.
* FastAPI backend.
* PostgreSQL persistence.
* pgvector-based retrieval.
* Transcript ingestion pipeline.
* LLM provider abstraction.
* Anthropic Claude provider.
* OpenAI provider.
* Ollama provider.
* Pi Coding Agent integration.
* Configuration-based provider selection.
* API validation and structured errors.
* SSE streaming.
* Health checks.
* Application logging.
* Automated testing.
* Docker Compose infrastructure.
* Sandboxed artifact rendering.

## Non-Goals

The project will not attempt to:

* Become a general-purpose AI assistant.
* Perform unrestricted external research.
* Train a foundation model.
* Build production-scale infrastructure.
* Implement billing.
* Execute arbitrary generated code.

---

# 5. Technical Decisions

## 5.1 Frontend

**React + Vite**

React with Vite is used for the conversational interface and Artifact Viewer.

The frontend provides:

* Chat interaction.
* Conversation history.
* Provider selection.
* Pi Agent mode.
* Streaming response rendering.
* Source display.
* Artifact viewing.

---

## 5.2 Database

**PostgreSQL + pgvector**

PostgreSQL is used for application persistence and is run locally through Docker Compose.

The database stores:

* Episode metadata.
* Transcript chunks.
* Vector embeddings.
* Conversations.
* Conversation messages.

pgvector is used for cosine-similarity-based transcript retrieval.

The current knowledge base contains:

* 50 podcast episodes
* 1,003 transcript chunks
* 1,003 embeddings

---

## 5.3 Agent Layer

**Pi Coding Agent**

The assignment allows either:

* Anthropic Claude Agent SDK, or
* Pi Coding Agent.

The implemented Growth Assistant uses **Pi Coding Agent**.

Pi is executed through its RPC interface as a subprocess.

The current local configuration uses:

* Provider: `ollama`
* Model: `llama3.2:3b`

Pi is currently started without its built-in tools for the local small-model configuration.

Transcript retrieval and factual grounding remain controlled by the application.

---

## 5.4 LLM Providers

The application supports:

* **Anthropic Claude**
* **OpenAI**
* **Ollama**

A provider abstraction and factory allow the application to select the requested provider without changing application source code.

The provider is selected explicitly by the user through the UI.

There is **no automatic provider fallback**.

If the selected provider is unavailable or not configured, the application reports the corresponding error.

---

## 5.5 Local LLM

**Ollama**

Ollama is used for the local demonstration.

The current models are:

* Chat model: `llama3.2:3b`
* Embedding model: `embeddinggemma`
* Embedding size: 768 dimensions

This allows the application to run locally without requiring a paid cloud API.

---

# 6. LLM Provider Behavior

The provider selection follows explicit user selection:

```text
User selects provider
        |
        v
+-------------------------------+
|                               |
v                               v
Ollama                        Cloud Provider
                                |
                         +------+------+
                         |             |
                         v             v
                       OpenAI        Claude
                         |             |
                         +------+------+
                                |
                                v
                         Provider Response
```

There is **no automatic fallback**.

For example:

```text
User selects Claude
        |
        v
Claude API key configured?
        |
    +---+---+
    |       |
   Yes      No
    |       |
    v       v
Claude   Configuration
response    error
```

The same behavior applies to OpenAI.

For the local demo:

```text
User selects Ollama
        |
        v
Ollama / llama3.2:3b
        |
        v
Response
```

When Pi Agent mode is enabled, the Growth Assistant uses Pi with Ollama and the normal provider selector is disabled.

---

# 7. Knowledge Base Architecture

The knowledge base is built from Lenny's Podcast/newsletter transcript repository.

The ingestion process is:

```text
Transcript Repository
        |
        v
Source Retrieval
        |
        v
Metadata Parsing
        |
        v
Transcript Parsing
        |
        v
Chunking
        |
        v
Embedding Generation
        |
        v
PostgreSQL + pgvector
```

The current local knowledge base contains:

* 50 episodes
* 1,003 transcript chunks
* 1,003 embeddings

The embedding model is:

```text
embeddinggemma
```

with:

```text
768 dimensions
```

---

# 8. Retrieval System

The retrieval flow is:

```text
User Question
      |
      v
Query Embedding
      |
      v
embeddinggemma
      |
      v
768-dimensional vector
      |
      v
PostgreSQL + pgvector
      |
      v
Cosine Similarity Search
      |
      v
Relevant Transcript Chunks
      |
      v
Grounded Context
      |
      v
LLM / Pi Agent
      |
      v
Grounded Response
```

The retrieval layer returns both transcript content and source metadata.

Source information includes:

* Episode title.
* Guest.
* Published date.
* Source URL.
* YouTube URL.
* Chunk index.
* Transcript content.
* Similarity distance.

---

# 9. Conversation & Session Architecture

Each conversation has a unique session ID.

The persistence model is:

```text
Conversation
    |
    +-- session_id
    +-- user_id
    +-- created_at
    +-- updated_at
    |
    +-- ConversationMessage
           |
           +-- role
           +-- content
           +-- created_at
```

When a user asks a follow-up question:

1. The existing conversation is loaded.
2. Previous messages are retrieved.
3. Previous messages are used to understand references.
4. Recent user messages are combined with the current question to improve retrieval.
5. New transcript evidence is retrieved.
6. The grounded agent generates the response.
7. The new assistant response is persisted.

Previous assistant responses are not treated as factual evidence.

Transcript retrieval remains the source of truth.

---

# 10. Streaming Architecture

Chat responses are streamed using Server-Sent Events.

```text
Frontend
    |
    v
FastAPI
    |
    v
Chat / Growth Assistant Service
    |
    v
LLM / Pi Agent
    |
    v
Response chunks
    |
    v
SSE
    |
    +---- token events
    |
    +---- sources event
    |
    +---- done event
    |
    v
React UI
```

Streaming allows the frontend to display generated content progressively.

---

# 11. Artifact Architecture

The application supports:

* Markdown artifacts.
* HTML/CSS artifacts.

The flow is:

```text
User Request
     |
     v
FastAPI Artifact API
     |
     v
Artifact Generation
     |
     v
Markdown / HTML
     |
     v
Artifact Viewer
```

Generated HTML is treated as untrusted content.

HTML artifacts are rendered inside a sandboxed iframe to isolate them from the parent application.

---

# 12. Ship 30 for 30

The application provides a dedicated Ship 30 for 30 capability.

The generation flow is:

```text
User Request
     |
     v
Relevant Transcript Retrieval
     |
     v
Ship 30 Writing Instructions
     |
     v
LLM Generation
     |
     v
Structured Newsletter Content
     |
     v
Chat / Artifact Output
```

The generated content is designed to include:

* Strong hook.
* Narrative structure.
* Clear headings.
* Skimmable sections.
* Bullets.
* Bold emphasis.
* Useful takeaway.
* Transcript-grounded claims.

The target output is approximately 1,250 words.

---

# 13. API Architecture

FastAPI exposes the application's HTTP API.

Primary routes include:

```text
GET  /health

POST /api/v1/chat
POST /api/v1/chat/stream

GET  /api/v1/conversations
GET  /api/v1/conversations/{session_id}

POST /api/v1/artifacts

POST /growth-assistant
POST /growth-assistant/stream
```

Pydantic schemas provide request validation and response contracts.

Streaming endpoints use Server-Sent Events.

---

# 14. Error Handling

The application handles common failure scenarios explicitly.

## Invalid Requests

Invalid or empty requests are rejected through validation.

## Missing Cloud API Keys

Claude and OpenAI providers validate their required API keys before generation.

## Provider Failures

Provider-specific failures are surfaced rather than triggering automatic fallback.

## Ollama Unavailable

If Ollama is unavailable, the selected request fails with an error.

## Empty Retrieval

If useful transcript context is not available, the assistant communicates that the available material is insufficient.

## Database Failures

Database sessions are cleaned up after operations, including streaming flows.

## Artifact Failures

Artifact generation failures are reported rather than presented as successful output.

---

# 15. Observability

The backend uses Python's standard logging system.

Important application events include:

* Chat requests.
* Selected provider.
* Streaming requests.
* HTTP/LLM activity.

Example:

```text
2026-09-05 12:06:58 | INFO | app.api.chat |
Streaming chat request received | provider=ollama
```

Uvicorn also provides application lifecycle and HTTP request logs.

---

# 16. Security

The application follows these security principles:

* API keys are stored in environment variables.
* `.env` is excluded from version control.
* Cloud API keys are not required for the Ollama demo.
* Generated HTML is treated as untrusted content.
* HTML artifacts are rendered inside a sandboxed iframe.
* Generated artifacts do not receive unrestricted access to the parent application.
* Previous assistant responses are not treated as factual grounding evidence.
* Provider selection is explicit.
* Transcript content is treated as knowledge-base context rather than executable code.

---

# 17. Deployment & Local Infrastructure

The database is containerized using Docker Compose.

```text
Docker Compose
      |
      v
PostgreSQL + pgvector
```

The local application environment consists of:

```text
React + Vite
      |
      v
FastAPI
      |
      +----------+
      |          |
      v          v
   Ollama    PostgreSQL
      |       + pgvector
      |
      +-- llama3.2:3b
      |
      +-- embeddinggemma
```

The frontend and backend run as local development processes.

Cloud providers can be enabled by supplying the corresponding API keys through environment variables.

---

# 18. Testing

The backend includes automated tests covering core application functionality.

The current test suite contains:

```text
23 passed
```

Test coverage includes areas such as:

* Retrieval context.
* Grounded agent behavior.
* Growth Assistant service.
* Pi Agent integration.
* API/service behavior.
* Core backend functionality.

Manual UI testing is also used to verify:

* Chat flow.
* Streaming responses.
* Conversation history.
* Source display.
* Provider selection.
* Pi Agent mode.
* Artifact generation.
* Artifact Viewer.
* Error states.

---

# 19. Current Implementation Status

The core implementation is complete.

```text
FastAPI Backend                 Complete
PostgreSQL + pgvector           Complete
Transcript ingestion            Complete
Vector retrieval                Complete
Grounded assistant              Complete
Persistent conversations        Complete
SSE streaming                   Complete
Pi Coding Agent integration     Complete
Ollama local demo               Complete
Claude provider                 Complete
OpenAI provider                 Complete
Ship 30 for 30                  Complete
Artifact generation             Complete
Artifact Viewer                 Complete
HTML sandboxing                 Complete
Application logging             Complete
Automated backend tests         Complete
Documentation                   In progress / final review
Demo recording                  Final preparation
```

The current implementation is focused on delivering a stable, evaluator-ready prototype that demonstrates grounded AI assistance, retrieval, agent architecture, provider flexibility, persistence, streaming, artifact generation, and operational considerations.
