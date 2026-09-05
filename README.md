
# Lenny Growth Assistant

An AI-powered conversational growth assistant grounded in Lenny's Podcast and newsletter transcripts.

The application helps users ask product and growth questions, receive grounded answers with source tracing, continue conversations across independent sessions, generate "Ship 30 for 30" content, and create Markdown or HTML/CSS artifacts rendered in an in-app viewer.

---

## 1. Project Overview

Lenny Growth Assistant is a full-stack AI application designed around one core principle:

> **When the available knowledge supports an answer, provide a useful grounded response with traceable sources. When it does not, clearly say so instead of inventing an answer.**

The application combines:

- Conversational AI
- Retrieval-augmented generation
- Lenny's Podcast and newsletter transcript knowledge base
- Persistent conversation sessions
- Multiple LLM providers
- Explicit provider selection
- Pi Coding Agent integration
- Artifact generation
- Sandboxed artifact rendering
- Streaming responses
- Source tracing

---

## 2. Key Features

### Grounded Conversational Assistant

Users can ask product and growth questions and receive answers grounded in the available Lenny transcript material.

The assistant:

- Retrieves relevant transcript content.
- Uses retrieved evidence when generating answers.
- Provides source information.
- Avoids unsupported claims.
- Clearly states when available material is insufficient.

### Independent Chat Sessions

Each new conversation receives its own session ID.

Follow-up questions within a session retain relevant conversation context, while new sessions start independently.

Conversation messages are persisted in PostgreSQL so users can return to previous conversations.

### LLM Provider Selection

The application supports three LLM providers:

- Anthropic Claude
- OpenAI
- Ollama

The provider is selected explicitly from the UI.

Claude and OpenAI provide cloud-based model execution, while Ollama provides a local model option.

#### Provider Behavior

The application does **not** automatically switch between providers.

If the selected cloud provider is not configured or cannot be used, the application returns a clear error instead of silently changing providers.

Ollama is the local provider used for the demo.

When Pi Agent mode is enabled, the application uses the local Ollama model through the Pi Coding Agent and the provider selector is disabled.

Example:

```text
User selects Ollama
        |
        v
Ollama
        |
        v
Response


User selects Claude
        |
        v
Claude API key configured?
        |
   +----+----+
   |         |
  Yes        No
   |         |
   v         v
Claude    Configuration
response     error


User selects OpenAI
        |
        v
OpenAI API key configured?
        |
   +----+----+
   |         |
  Yes        No
   |         |
   v         v
OpenAI    Configuration
response     error
````

### Pi Coding Agent Mode

The application supports a Pi Coding Agent mode for the Growth Assistant flow.

When Pi Agent mode is enabled:

* The application uses the Pi Coding Agent.
* The local Ollama model is used for the demo.
* The provider selector is disabled.
* Transcript retrieval remains the source of factual grounding.
* Conversation context is preserved across follow-up questions.

Pi is used as the agent layer while the application retains control over transcript retrieval and the final grounded response flow.

### Transcript Knowledge Base

The application uses Lenny's Podcast transcript repository as its knowledge base.

The ingestion pipeline:

1. Retrieves transcript data.
2. Parses episode metadata and transcript content.
3. Splits transcripts into overlapping chunks.
4. Generates embeddings using Ollama.
5. Stores transcript chunks and embeddings in PostgreSQL with pgvector.

The current local knowledge base contains:

* 50 podcast episodes
* 1,003 transcript chunks
* 1,003 generated embeddings

The embedding model used by the demo is:

```text
embeddinggemma
```

with 768-dimensional embeddings.

### Vector Retrieval

User questions are converted into embeddings and searched against the transcript knowledge base using vector similarity.

```text
User question
      |
      v
Ollama embedding
      |
      v
Vector similarity search
      |
      v
PostgreSQL + pgvector
      |
      v
Relevant transcript chunks
      |
      v
Grounded assistant response
```

Retrieved sources are returned to the frontend so users can trace the answer back to the relevant episode and transcript sections.

### Conversation History and Follow-ups

The application supports persistent conversational sessions.

Each conversation has a unique session ID.

The system stores:

* Conversation/session metadata
* User messages
* Assistant messages
* Creation and update timestamps

For follow-up questions, previous conversation messages are used to understand references and context.

Previous assistant responses are **not treated as factual evidence**. Transcript retrieval remains the source of truth for grounded answers.

### Streaming Responses

Assistant responses are streamed to the frontend using Server-Sent Events (SSE).

```text
Frontend
    |
    v
FastAPI
    |
    v
Agent / LLM
    |
    v
Token chunks
    |
    v
SSE
    |
    v
Frontend chat interface
```

The frontend displays the response progressively instead of waiting for the complete generation.

### Ship 30 for 30

The application includes a dedicated "Ship 30 for 30" capability for generating newsletter-style content grounded in Lenny's transcript material.

The skill focuses on:

* Strong hooks
* Clear narrative structure
* Skimmable headings
* Bullets and emphasis
* Useful takeaways
* Transcript-grounded claims

The generated content is designed to be approximately 1,250 words while remaining readable and actionable.

### Artifact Generation

The application can generate:

* Markdown artifacts
* HTML/CSS artifacts

Generated artifacts are displayed in an Artifact Viewer alongside the conversation.

HTML artifacts are rendered inside a sandboxed iframe to isolate generated content from the main application.

### Artifact Viewer Security

Generated HTML is treated as untrusted content.

The viewer uses browser sandboxing to isolate generated artifacts from the main application.

The generated artifact does not receive unrestricted access to the parent application environment.

---

## 3. API

The backend is implemented using FastAPI.

Main API capabilities include:

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

The API uses Pydantic request/response models for validation and structured response contracts.

---

## 4. Database

PostgreSQL is used for application persistence.

The database stores:

* Episodes
* Transcript chunks
* Vector embeddings
* Conversations
* Conversation messages

`pgvector` is used for vector similarity search.

The database is started using Docker Compose.

---

## 5. Logging

The application uses Python's built-in logging system for application-level operational logs.

Important application events include:

* Chat requests
* Selected LLM provider
* Streaming requests
* HTTP/LLM request activity

Example:

```text
2026-09-05 12:06:58 | INFO | app.api.chat | Streaming chat request received | provider=ollama
```

The application also exposes normal Uvicorn request and startup logs.

---

## 6. Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic
* PostgreSQL
* pgvector

### AI / Agent Layer

* Ollama
* Llama 3.2 3B
* embeddinggemma
* Pi Coding Agent
* Anthropic Claude
* OpenAI

### Frontend

* React
* Vite
* JavaScript
* CSS

### Infrastructure

* Docker
* Docker Compose
* PostgreSQL
* Git / GitHub

---

## 7. Project Structure

```text
lenny-growth-assistant/
|
+-- backend/
|   +-- app/
|   |   +-- agent/
|   |   +-- api/
|   |   +-- db/
|   |   +-- embeddings/
|   |   +-- ingestion/
|   |   +-- llm/
|   |   +-- models/
|   |   +-- repositories/
|   |   +-- retrieval/
|   |   +-- schemas/
|   |   +-- services/
|   |
|   +-- alembic/
|   +-- tests/
|   +-- pyproject.toml
|   +-- requirements.txt
|
+-- frontend/
|   +-- src/
|   +-- package.json
|   +-- vite.config.js
|
+-- data/
|   +-- lenny-transcripts/
|
+-- docs/
|   +-- PRD.md
|   +-- design.md
|   +-- architecture.md
|   +-- PROJECT_SPEC.md
|
+-- docker-compose.yml
+-- .env
+-- .gitignore
+-- README.md
```

---

## 8. Local Setup

### Prerequisites

Install:

* Python 3.11+
* Node.js
* npm
* Docker Desktop
* Ollama
* Git

### 8.1 Clone the Repository

```bash
git clone https://github.com/Pavani-A/lenny-growth-assistant.git
cd lenny-growth-assistant
```

### 8.2 Start PostgreSQL

From the project root:

```bash
docker compose up -d
```

Check that the database container is running:

```bash
docker ps
```

### 8.3 Install Ollama Models

The demo uses:

```bash
ollama pull llama3.2:3b
ollama pull embeddinggemma
```

Make sure Ollama is running before starting the backend.

### 8.4 Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create and activate a virtual environment.

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

### 8.5 Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg://lenny_user:lenny_password@localhost:5432/lenny_growth

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_EMBEDDING_MODEL=embeddinggemma
OLLAMA_TIMEOUT=300

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-3-5-haiku-latest
```

Cloud API keys are optional for the local Ollama demo.

**Never commit real API keys to GitHub.**

### 8.6 Database Migration

From the backend directory:

```bash
alembic upgrade head
```

### 8.7 Run the Backend

From the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 8.8 Run the Frontend

Open a second terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## 9. Transcript Ingestion

The project includes an ingestion pipeline for loading Lenny transcript data into PostgreSQL.

The pipeline performs:

```text
Transcript repository
        |
        v
Metadata parsing
        |
        v
Transcript parsing
        |
        v
Chunking
        |
        v
Embedding generation
        |
        v
PostgreSQL + pgvector
```

The transcript source is the Lenny Podcast/newsletter data repository.

The ingestion pipeline can be refreshed when new transcript material becomes available.

---

## 10. Testing

The backend includes automated tests covering core application functionality.

Run the full test suite from the backend directory:

```bash
pytest -q
```

Current test status:

```text
23 passed
```

The test suite covers areas including:

* Retrieval context
* Grounded agent behavior
* Growth Assistant service
* Pi Agent integration
* API/service behavior
* Other backend functionality

---

## 11. Resilience and Error Handling

The application handles several failure scenarios explicitly.

### Missing Cloud API Keys

If Claude or OpenAI is selected without the required API key, the application reports a configuration error.

### Ollama Unavailable

If the local Ollama service is unavailable, the request fails with an error rather than silently switching providers.

### Empty or Invalid Requests

API request validation rejects invalid input.

### Empty Retrieval

If relevant transcript material cannot be found, the assistant clearly states that the available transcript material does not provide enough evidence.

### Database Failures

Database operations use SQLAlchemy sessions with controlled cleanup.

### Provider Failures

Provider-specific errors are surfaced through structured API errors rather than hidden automatic provider switching.

---

## 12. Design and Architecture Documentation

Additional project documentation is available in the `docs/` directory:

* `docs/PRD.md` — Product requirements and discovery brief
* `docs/design.md` — Product and interface design
* `docs/architecture.md` — Technical architecture
* `docs/PROJECT_SPEC.md` — Project implementation specification

---

## 13. Demo Flow

The recommended demo flow is:

1. Open the Lenny Growth Assistant.
2. Ask a product/growth question.
3. Show the grounded response.
4. Show the retrieved transcript sources.
5. Ask a follow-up question to demonstrate conversation context.
6. Show conversation history.
7. Enable Pi Agent mode.
8. Ask another grounded question.
9. Generate a Ship 30 for 30 artifact.
10. Open the Artifact Viewer.
11. Demonstrate provider selection and configuration-error handling if needed.

The local Ollama configuration is recommended for the demo because it does not require a paid cloud API key.

---

## 14. Security Considerations

* API keys are stored in environment variables.
* `.env` is excluded from version control.
* Generated HTML artifacts are rendered in a sandboxed iframe.
* Transcript data is treated as knowledge-base content rather than executable code.
* Previous assistant responses are not treated as factual grounding evidence.
* The application does not automatically switch providers without user selection.

---

## 15. License and Source Data

The transcript knowledge base is derived from the Lenny Podcast/newsletter transcript repository used for this assignment.

Refer to the source repository's licensing terms before redistributing transcript data or using it outside the intended project context.



