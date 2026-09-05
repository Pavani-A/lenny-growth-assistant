
# Lenny Growth Assistant — Technical Architecture

## 1. Architecture Overview

Lenny Growth Assistant is a full-stack AI conversational application that answers product and growth questions using a grounded knowledge base built from Lenny's Podcast and newsletter transcripts.

The system is designed around five core principles:

1. **Grounded answers** — responses should be supported by available transcript material.

2. **Session-aware conversations** — follow-up questions maintain the context of the current chat session.

3. **Provider flexibility** — the application supports Anthropic Claude, OpenAI, and local Ollama through explicit provider selection without changing application code.

4. **Artifact-first output** — the assistant can generate Markdown or HTML/CSS artifacts that are rendered in a dedicated viewer.

5. **Operational simplicity** — the application can be run locally with PostgreSQL through Docker Compose, with the backend and frontend started independently.

---

## 2. High-Level System Architecture

```text
                                      ┌───────────────────────┐
                                      │         User          │
                                      └───────────┬───────────┘
                                                  │
                                                  ▼
                                      ┌───────────────────────┐
                                      │   React + Vite UI      │
                                      │                       │
                                      │  Chat UI              │
                                      │  Conversation History │
                                      │  Provider Selector    │
                                      │  Pi Agent Toggle      │
                                      │  Source Display       │
                                      │  Artifact Viewer      │
                                      └───────────┬───────────┘
                                                  │
                                      HTTP / JSON / SSE
                                                  │
                                                  ▼
                                      ┌───────────────────────┐
                                      │    FastAPI Backend    │
                                      │                       │
                                      │  API Routes           │
                                      │  Request Validation   │
                                      │  Session Handling     │
                                      │  Streaming            │
                                      │  Error Handling       │
                                      └───────────┬───────────┘
                                                  │
                         ┌────────────────────────┼────────────────────────┐
                         │                        │                        │
                         ▼                        ▼                        ▼
              ┌───────────────────┐   ┌────────────────────┐   ┌───────────────────┐
              │ Standard Chat     │   │ Growth Assistant   │   │ Artifact Service  │
              │ Service           │   │ Service            │   │                   │
              │                   │   │                    │   │ Markdown / HTML   │
              │ Provider Factory  │   │ Pi Agent           │   │ Artifact creation │
              │ Retrieval         │   │ Grounded Agent     │   │                   │
              │ Persistence       │   │ Retrieval          │   │                   │
              └─────────┬─────────┘   └──────────┬─────────┘   └───────────────────┘
                        │                        │
                        │                        │
                        ▼                        ▼
              ┌────────────────────────────────────────────┐
              │              LLM / Agent Layer              │
              │                                            │
              │  Ollama Provider                           │
              │  OpenAI Provider                           │
              │  Claude Provider                           │
              │  Pi Coding Agent                           │
              └──────────────────────┬─────────────────────┘
                                     │
                                     ▼
                         ┌─────────────────────────┐
                         │      Ollama / Models    │
                         │                         │
                         │  llama3.2:3b             │
                         │  embeddinggemma           │
                         └────────────┬────────────┘
                                      │
                                      │ Embeddings /
                                      │ Generation
                                      ▼
                         ┌─────────────────────────┐
                         │   Retrieval Layer       │
                         │                         │
                         │  Query Embedding        │
                         │  Vector Similarity      │
                         │  Context Construction   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ PostgreSQL + pgvector   │
                         │                         │
                         │ Episodes                │
                         │ Transcript Chunks       │
                         │ Embeddings              │
                         │ Conversations           │
                         │ Messages                │
                         └─────────────────────────┘
````

---

## 3. Frontend Architecture

The frontend is implemented using React and Vite.

The primary responsibilities of the frontend are:

* Chat interaction
* Conversation creation and selection
* Conversation history display
* Provider selection
* Pi Agent mode selection
* Streaming response rendering
* Source display
* Artifact generation
* Artifact viewing

### Provider Selection

The UI provides explicit selection between:

* Ollama
* Claude
* OpenAI

The selected provider is sent with the chat request.

There is **no automatic provider fallback**.

If a selected cloud provider is unavailable or its API key is not configured, the frontend displays the corresponding configuration/error state.

### Pi Agent Mode

The frontend also provides a Pi Agent mode.

When enabled:

* Pi Coding Agent is used for the Growth Assistant flow.
* Ollama is used as the local model provider.
* The normal provider selector is disabled.
* Conversation session context remains available.
* Transcript retrieval continues to provide the factual grounding.

---

## 4. Backend Architecture

The backend is implemented using FastAPI.

The application is organized into separate layers for API handling, services, agents, retrieval, LLM providers, persistence, and schemas.

```text
backend/app/
|
+-- agent/
|   +-- grounded_agent.py
|   +-- pi_agent.py
|
+-- api/
|   +-- chat.py
|   +-- conversations.py
|   +-- artifact.py
|   +-- growth_assistant.py
|
+-- db/
|   +-- database.py
|
+-- embeddings/
|   +-- ollama_embeddings.py
|
+-- ingestion/
|
+-- llm/
|   +-- base.py
|   +-- ollama.py
|   +-- openai_provider.py
|   +-- claude_provider.py
|   +-- factory.py
|
+-- models/
|
+-- repositories/
|
+-- retrieval/
|   +-- search.py
|   +-- context.py
|
+-- schemas/
|
+-- services/
|   +-- chat_service.py
|   +-- growth_assistant_service.py
```

---

## 5. LLM Provider Architecture

The application uses a common provider abstraction so that the application can work with multiple LLM providers.

```text
                     ┌──────────────────────┐
                     │    LLMProvider       │
                     │    abstraction       │
                     └──────────┬───────────┘
                                │
               ┌────────────────┼────────────────┐
               │                │                │
               ▼                ▼                ▼
       ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
       │    Ollama     │ │    OpenAI     │ │    Claude     │
       │   Provider    │ │   Provider    │ │   Provider    │
       └───────────────┘ └───────────────┘ └───────────────┘
```

The provider factory selects the implementation based on the provider requested by the application.

Supported provider values are:

```text
ollama
openai
claude
```

The selected provider is used directly.

The system intentionally does **not** implement automatic fallback from one provider to another. This makes provider behavior predictable and visible to the user.

---

## 6. Pi Coding Agent Architecture

The Growth Assistant has a separate Pi Coding Agent execution path.

```text
User
 |
 v
FastAPI Growth Assistant API
 |
 v
GrowthAssistantService
 |
 v
GroundedLennyAgent
 |
 +----------------------+
 |                      |
 v                      v
Transcript Retrieval   Pi Coding Agent
 |                      |
 v                      v
Grounded Context       Ollama / Llama 3.2 3B
 |                      |
 +----------+-----------+
            |
            v
     Grounded Response
            |
            v
          User
```

The Pi Agent is executed as a subprocess using Pi's RPC mode.

The application communicates with Pi using newline-delimited JSON messages.

For the current local configuration, Pi uses:

```text
Provider: ollama
Model: llama3.2:3b
```

Pi is started without its built-in tools for the current small local model configuration. Transcript retrieval and grounding remain controlled by the application.

---

## 7. Retrieval Architecture

The retrieval pipeline is responsible for finding relevant transcript material before response generation.

```text
User Question
     |
     v
Embedding Service
     |
     v
embeddinggemma
     |
     v
768-dimensional query vector
     |
     v
PostgreSQL + pgvector
     |
     v
Cosine Similarity Search
     |
     v
Top Relevant Transcript Chunks
     |
     v
Grounded Context
     |
     v
Agent / LLM
```

The retrieval layer returns transcript metadata together with the retrieved content.

Source information includes:

* Episode title
* Guest
* Publication date
* Source URL
* YouTube URL
* Chunk index
* Transcript content
* Similarity distance

This information is passed back to the frontend so that generated answers can be traced to the retrieved transcript material.

---

## 8. Conversation and Session Architecture

Each conversation is identified by a unique session ID.

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

Conversation messages are stored in PostgreSQL.

For follow-up questions:

1. The existing conversation is loaded using the session ID.
2. Previous messages are retrieved.
3. Previous messages are used to understand references and conversational context.
4. A retrieval query is constructed using recent user messages and the current question.
5. New transcript evidence is retrieved.
6. The agent generates the response using the current transcript context.

Previous assistant responses are not treated as factual evidence.

The transcript knowledge base remains the source of truth.

---

## 9. Streaming Architecture

Chat responses are streamed using Server-Sent Events (SSE).

```text
Frontend
   |
   | POST request
   v
FastAPI
   |
   v
Chat / Growth Assistant Service
   |
   v
LLM / Pi Agent
   |
   | response chunks
   v
SSE event stream
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

The frontend renders token chunks as they arrive.

After generation completes, source information is sent as a separate SSE event followed by a completion event.

This allows the interface to display the response progressively while still presenting source information after generation.

---

## 10. Transcript Ingestion Architecture

Transcript ingestion is a separate pipeline used to populate the knowledge base.

```text
Lenny Transcript Repository
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
       PostgreSQL
            |
            v
        pgvector
```

The ingestion process:

1. Retrieves transcript data.
2. Parses episode metadata.
3. Extracts transcript content.
4. Splits transcripts into overlapping chunks.
5. Generates embeddings using `embeddinggemma`.
6. Stores episodes, chunks, and embeddings in PostgreSQL.

The current knowledge base contains:

```text
50 episodes
1,003 transcript chunks
1,003 embeddings
```

The embedding dimension is:

```text
768
```

---

## 11. Artifact Architecture

Artifact generation is exposed through the backend artifact API.

The application supports:

* Markdown artifacts
* HTML/CSS artifacts

The general flow is:

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
Frontend Artifact Viewer
```

HTML artifacts are rendered inside a sandboxed iframe.

Generated HTML is treated as untrusted content and is isolated from the parent application using browser sandboxing.

The viewer therefore does not give generated HTML unrestricted access to the main application context.

---

## 12. Ship 30 for 30 Architecture

The Ship 30 for 30 functionality is implemented as a dedicated skill/capability within the application.

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
Artifact / Chat Output
```

The generated content is designed around:

* Strong hooks
* Narrative structure
* Skimmable sections
* Headings
* Bullets
* Bold emphasis
* Useful takeaways
* Transcript-grounded claims

The target output length is approximately 1,250 words.

---

## 13. Database Architecture

PostgreSQL is the persistence layer for the application.

The database contains the following primary entities:

```text
Episode
   |
   +-- TranscriptChunk
          |
          +-- embedding

Conversation
   |
   +-- ConversationMessage
```

### Episode

Stores metadata about each podcast episode, including:

* Title
* Guest
* Description
* Published date
* Source URL
* YouTube URL
* Transcript filename
* Word count
* Timestamps

### TranscriptChunk

Stores:

* Episode relationship
* Chunk index
* Transcript content
* Vector embedding
* Creation timestamp

### Conversation

Stores:

* Session ID
* User ID
* Creation timestamp
* Update timestamp

### ConversationMessage

Stores:

* Conversation relationship
* Role
* Message content
* Creation timestamp

---

## 14. API Architecture

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

## 15. Error Handling and Resilience

The architecture explicitly handles common operational failures.

### Invalid Requests

Pydantic validation and service-level validation reject empty or invalid input.

### Missing Cloud API Keys

Claude and OpenAI providers validate their required API keys before attempting generation.

### Provider Failures

Provider-specific failures are surfaced to the application instead of triggering an automatic provider switch.

### Ollama Unavailable

If Ollama is unavailable, the selected Ollama request fails rather than silently switching to a cloud provider.

### Empty Retrieval

If no useful transcript context is found, the assistant returns a clear message indicating that the available transcript material is insufficient.

### Database Cleanup

Database sessions are explicitly closed after operations, including streaming flows.

---

## 16. Observability

The backend uses Python's standard logging system.

Important events include:

* Chat requests
* Selected provider
* Streaming requests
* HTTP/LLM activity

Example:

```text
2026-09-05 12:06:58 | INFO | app.api.chat |
Streaming chat request received | provider=ollama
```

Uvicorn also provides HTTP request and application lifecycle logs.

---

## 17. Deployment and Local Infrastructure

PostgreSQL is containerized using Docker Compose.

```text
Docker Compose
      |
      v
PostgreSQL + pgvector
```

The frontend and backend run as local development processes.

The local demo environment consists of:

```text
React + Vite
     |
FastAPI
     |
Ollama
     |
PostgreSQL + pgvector
```

Ollama provides:

```text
Chat model:      llama3.2:3b
Embedding model: embeddinggemma
```

The cloud providers can be enabled by supplying their corresponding API keys through environment variables.

---

## 18. Security Considerations

The architecture includes several security considerations:

* API keys are stored in environment variables.
* `.env` is excluded from version control.
* Cloud API keys are not required for the local Ollama demo.
* Generated HTML is treated as untrusted content.
* HTML artifacts are rendered using a sandboxed iframe.
* Previous assistant messages are not used as factual grounding evidence.
* Provider selection is explicit rather than automatic.
* Transcript content is used as knowledge-base context and is not executed as application code.


