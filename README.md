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
- Provider fallback
- Artifact generation
- Sandboxed artifact rendering

---

# 2. Key Features

## Grounded Conversational Assistant

Users can ask product and growth questions and receive answers grounded in the available Lenny transcript material.

The assistant:

- Retrieves relevant transcript content.
- Uses retrieved evidence when generating answers.
- Provides source information.
- Avoids unsupported claims.
- Clearly states when available material is insufficient.

---

## Independent Chat Sessions

Each new conversation receives its own session ID.

Follow-up questions within a session retain relevant context, while new sessions start independently.

---

## LLM Provider Selection

The application supports three LLM providers:

- Anthropic Claude
- OpenAI
- Ollama

The user can select a preferred provider from the UI.

Claude and OpenAI provide cloud-based model execution, while Ollama provides a local model option.

---

## Provider Fallback

The application includes a resilient provider fallback strategy.

The user's selected provider is treated as the preferred provider.

If the preferred cloud provider fails because of a provider or infrastructure problem, the system can attempt another configured cloud provider.

If the cloud providers are unavailable or fail, the system falls back to Ollama.

Example:

```text
Claude selected
      ↓
Claude request
      ↓
Failure
      ↓
OpenAI configured?
      ↓
OpenAI request
      ↓
Failure
      ↓
Ollama