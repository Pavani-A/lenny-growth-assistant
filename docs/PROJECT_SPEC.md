# Lenny Growth Assistant — Project Specification

## 1. Product Overview

### Product Name

**The Lenny Growth Assistant**

### Product Description

The Lenny Growth Assistant is a full-stack AI conversational application that helps users answer product and growth questions using knowledge grounded in Lenny's Podcast transcripts.

Users can:

- Ask product and growth questions.
- Receive answers grounded in transcript content.
- View supporting sources.
- Continue conversations with preserved context.
- Generate Ship 30 for 30-style content.
- Generate Markdown or HTML/CSS artifacts.
- View generated artifacts inside the application.

### Core Product Principle

> **Grounded usefulness over confident guessing.**

If the available transcript material does not support an answer, the assistant should clearly say that it does not have enough information rather than inventing an answer.

---

# 2. Users & Problem

## Primary Users

- Product Managers
- Founders and startup teams
- Growth professionals

## User Problem

Lenny's Podcast contains a large amount of product, growth, leadership, and startup knowledge.

Finding relevant information manually across transcripts can be time-consuming. A general-purpose AI assistant may also provide answers that are not supported by Lenny's content.

## Solution

The Lenny Growth Assistant provides a conversational interface over the transcript knowledge base so users can ask questions naturally and receive grounded answers with supporting sources.

---

# 3. Discovery Brief

## Success Metrics

### Grounded Answer Rate

Target: **≥90%**

Measure the percentage of supported questions that receive answers grounded in relevant transcript evidence.

### Unsupported Question Safety Rate

Target: **100%**

For deliberately unsupported questions, the assistant should avoid presenting unsupported information as though it came from Lenny's content.

### Core Flow Completion

The evaluator should be able to successfully complete the main product flows:

- Start a chat.
- Ask a grounded question.
- View the supporting source.
- Ask a follow-up question.
- Ask an unsupported question.
- Generate a Ship 30 for 30 article.
- Generate an artifact.
- View the artifact.

## Assumptions

- Lenny Podcast/newsletter transcript content is available for the project.
- A curated transcript repository is sufficient for the initial implementation.
- PostgreSQL will be used for persistence.
- Local PostgreSQL will run through Docker Compose.
- Ollama will be available for the required local demonstration.
- At least one cloud LLM provider can be configured.
- No model fine-tuning is required.
- Generated HTML/CSS will be treated as untrusted content.
- The project is an evaluator-ready prototype rather than production-scale SaaS.

## Scope

### In Scope

- Grounded conversational assistant.
- Independent chat sessions.
- PostgreSQL persistence.
- Transcript ingestion and retrieval.
- Source tracing.
- Follow-up conversation context.
- Claude Agent SDK.
- Anthropic Claude support.
- OpenAI support.
- Ollama support.
- LLM provider configuration.
- Ship 30 for 30 skill/tool.
- Markdown artifacts.
- HTML/CSS artifacts.
- In-app Artifact Viewer.
- API validation.
- Structured errors.
- Health endpoints.
- Structured logging.
- Automated tests.
- Docker Compose startup.
- Documentation.

### Out of Scope

- General-purpose AI assistant.
- Unrestricted web search.
- Foundation-model training or fine-tuning.
- Production-scale SaaS infrastructure.
- Production billing.
- Arbitrary code execution.
- Native mobile applications.

## Key Risks

- Hallucination.
- Poor transcript retrieval.
- Local model quality.
- Model latency.
- Cloud API cost.
- Ollama unavailable.
- Database failures.
- Stale transcript data.
- Unsafe HTML rendering.

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
9. Provide a reproducible and testable project.

## Technical Goals

- React + Vite frontend.
- FastAPI backend.
- PostgreSQL persistence.
- Retrieval-based knowledge system.
- Anthropic Claude Agent SDK.
- Claude and OpenAI cloud providers.
- Ollama local provider.
- Configuration-based provider selection.
- API validation and structured errors.
- Health checks and logging.
- Automated testing.
- Docker Compose startup.

## Non-Goals

The project will not attempt to:

- Become a general-purpose AI assistant.
- Perform unrestricted external research.
- Train a foundation model.
- Build production-scale infrastructure.
- Implement billing.
- Execute arbitrary generated code.

---

# 5. Technical Decisions

## 5.1 Frontend

**React (Vite)**

The assignment does not specify a frontend framework.

React with Vite will be used because it best supports the conversational interface and Claude-Artifacts-style side-by-side Artifact Viewer requested by the assignment.

---

## 5.2 Database

**PostgreSQL running locally through Docker Compose**

The assignment requires conversations to be stored in PostgreSQL and mentions Supabase or Railway as possible options.

The default implementation will use local PostgreSQL through Docker Compose so the project can be started without external accounts.

Supabase and Railway will be documented as alternative PostgreSQL deployment options in the README.

---

## 5.3 Agent Layer

**Anthropic Claude Agent SDK**

The assignment requires the agent layer to use either:

- Anthropic Claude Agent SDK, or
- Pi Coding Agent.

This project will use the **Anthropic Claude Agent SDK**.

---

## 5.4 Cloud LLM

The application will support both:

- **Anthropic Claude**
- **OpenAI**

A provider toggle/configuration will allow the application to use either cloud provider.

The application will default to whichever configured cloud provider key is present in `.env`.

If neither cloud provider key is configured, the application will use Ollama.

Provider/model configuration will not require changes to application source code.

---

## 5.5 Local LLM

**Ollama**

Ollama is mandatory for the demonstration.

It provides a local LLM option so the application can be demonstrated without depending entirely on a cloud API.

---

# 6. LLM Provider Behavior

The provider selection will follow this behavior:

```text
Check .env configuration
        ↓
Is Anthropic key available?
        ↓
      Yes → Use Anthropic Claude
        │
        No
        ↓
Is OpenAI key available?
        ↓
      Yes → Use OpenAI
        │
        No
        ↓
Use Ollama