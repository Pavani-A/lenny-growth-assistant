# Lenny Growth Assistant — Technical Architecture

## 1. Architecture Overview

Lenny Growth Assistant is a full-stack AI conversational application that answers product and growth questions using a grounded knowledge base built from Lenny's Podcast and newsletter transcripts.

The system is designed around five core principles:

1. **Grounded answers** — responses should be supported by available transcript material.
2. **Session-aware conversations** — follow-up questions maintain the context of the current chat session.
3. **Provider flexibility** — the application can use Anthropic Claude, OpenAI, or local Ollama without changing application code.
4. **Artifact-first output** — the assistant can generate Markdown or HTML/CSS artifacts that are rendered in a dedicated viewer.
5. **Operational simplicity** — the complete application should be runnable locally using Docker Compose.

---

## 2. High-Level System Architecture

```text
                                                ┌──────────────────────────┐
                         │          User            │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │    React + Vite Frontend │
                         │                          │
                         │  Chat UI                 │
                         │  Session List            │
                         │  Provider Selector       │
                         │  Source Display          │
                         │  Artifact Viewer         │
                         └────────────┬─────────────┘
                                      │ HTTP / JSON
                                      ▼
                         ┌──────────────────────────┐
                         │      FastAPI Backend     │
                         │                          │
                         │  API Routes              │
                         │  Validation              │
                         │  Session Management      │
                         │  Error Handling           │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                    ┌────────────────────────────────────┐
                    │      Agent / Orchestration Layer   │
                    │                                    │
                    │  Anthropic Claude Agent SDK        │
                    │  Tool Selection                    │
                    │  Retrieval                         │
                    │  Grounding                         │
                    │  Artifact Generation               │
                    └───────────────┬────────────────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ Anthropic Claude│    │ OpenAI          │    │ Ollama          │
    │ Preferred Cloud │    │ Preferred Cloud │    │ Local Fallback  │
    │ Provider        │    │ Provider        │    │ Provider        │
    └────────┬────────┘    └────────┬────────┘    └────────▲────────┘
             │                      │                      │
             │      Cloud provider fails                  │
             └──────────────────────┴──────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────────┐
                         │   Ollama / Llama         │
                         │   Final Local Fallback   │
                         └──────────────────────────┘

                                    │
                                    ▼
                         ┌──────────────────────────┐
                         │ PostgreSQL + pgvector    │
                         │                          │
                         │ Sessions                 │
                         │ Messages                 │
                         │ Sources                  │
                         │ Transcript Chunks        │
                         │ Embeddings               │
                         │ Artifacts                │
                         └──────────────────────────┘