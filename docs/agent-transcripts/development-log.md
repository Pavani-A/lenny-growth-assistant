# Lenny Growth Assistant — Agent Transcripts & Development Corrections

## 1. Purpose

This document records important agentic development attempts, failures, debugging steps, and corrections made while building the Lenny Growth Assistant.

The goal is to provide transparency into the development process and show how implementation decisions were validated and corrected rather than hiding failed approaches.

---

# 2. Pi Coding Agent Integration

## Initial Approach

The assignment required the agent layer to use either the Anthropic Claude Agent SDK or Pi Coding Agent.

Pi Coding Agent was selected because it allowed the project to demonstrate an agent-based architecture while keeping the required local Ollama demonstration possible.

The initial implementation attempted to run Pi against the local Ollama model:

```text
Provider: ollama
Model: llama3.2:3b
```

---

# 3. Failed Attempt — Pi Tool Calling

## Problem

The initial Pi configuration allowed the model to use Pi's built-in tools.

During testing, the local `llama3.2:3b` model attempted to produce an invalid tool command instead of following the expected interaction flow.

The issue was caused by the combination of:

* A relatively small local model.
* Pi's tool-calling interface.
* The model attempting to invoke tools incorrectly.

## Observation

The model did not reliably understand the available tool interface.

This made the approach unsuitable for a stable evaluator demonstration.

## Correction

Pi was changed to run with:

```text
--no-tools
```

This kept Pi responsible for the agent execution while the application itself controlled:

* Transcript retrieval.
* Grounding context.
* Conversation history.
* Source tracing.

## Result

The Pi Agent flow became stable with the local Ollama model.

---

# 4. Failed Attempt — Windows Pi Process Execution

## Problem

The first subprocess implementation assumed that the Pi executable could be invoked directly using the normal executable name.

On Windows, the installed npm command resolved through:

```text
pi.cmd
```

rather than a native executable.

## Correction

The Pi integration was updated to invoke the Windows command file explicitly.

The subprocess was also configured with:

```text
text=True
encoding="utf-8"
```

This ensured that JSONL messages exchanged with the Pi RPC process were decoded correctly.

## Result

Pi RPC communication worked reliably from the FastAPI backend.

---

# 5. Pi RPC Protocol

## Implementation

Pi was integrated through its RPC mode.

The backend starts Pi with the required provider and model configuration and communicates through newline-delimited JSON.

The application sends a prompt event and listens for Pi response events.

The response stream processes assistant text deltas until the agent reports completion.

This allows the backend to expose the generated response through the application's existing API layer.

---

# 6. Retrieval Grounding

## Initial Approach

The Growth Assistant initially retrieved transcript context directly from the current user question.

This worked for independent questions but was insufficient for some conversational follow-ups.

For example:

```text
User:
What did the guests say about product-led growth?

Assistant:
...

User:
What about the second approach?
```

The second question may not contain enough information by itself to retrieve the correct transcript content.

## Correction

Conversation history was incorporated into the retrieval query.

The current implementation considers recent user messages together with the current question when constructing the retrieval query.

The previous conversation is also supplied to the agent so that references and follow-up questions can be understood.

However, previous assistant responses are explicitly not treated as factual evidence.

## Result

Follow-up questions can preserve conversational meaning while continuing to use transcript retrieval as the factual source of truth.

---

# 7. Grounding Rule Correction

## Problem

Conversation history can contain previous assistant-generated information.

Treating the entire conversation history as factual context could allow an unsupported claim from an earlier response to become evidence for a later response.

## Correction

The agent prompt explicitly separates:

```text
PREVIOUS CONVERSATION
```

from:

```text
RETRIEVED TRANSCRIPT CONTEXT
```

The instructions state that conversation history may only be used to understand references and follow-up questions.

Transcript context remains the only factual evidence.

## Result

The architecture preserves conversational continuity without allowing previous model output to become an uncontrolled knowledge source.

---

# 8. LLM Provider Architecture

## Initial Design Consideration

The application originally considered automatically selecting a cloud provider based on which API key was available.

This would have created behavior such as:

```text
Anthropic key available → Claude
otherwise
OpenAI key available → OpenAI
otherwise
Ollama
```

## Correction

The final implementation uses explicit provider selection.

The user can select:

* Ollama
* Claude
* OpenAI

The application does not automatically switch providers when the selected provider fails.

## Reason

Explicit selection makes provider behavior predictable and easier to demonstrate and debug.

It also avoids silently changing the model used for a request.

---

# 9. Cloud Provider Configuration

## Problem

The local demonstration does not require paid cloud APIs, but the assignment requires cloud provider support.

The implementation therefore needed to support cloud providers without making them mandatory for the local demo.

## Correction

Claude and OpenAI providers validate their respective environment variables when selected.

For example:

```text
ANTHROPIC_API_KEY
OPENAI_API_KEY
```

If the selected provider is not configured, the application reports a configuration error.

Ollama remains available for the local demonstration.

---

# 10. Artifact Security

## Design Decision

Generated HTML/CSS artifacts are untrusted content.

Rendering generated HTML directly inside the parent application could allow generated content to interact with the application's DOM or environment.

## Correction

The Artifact Viewer renders HTML inside a sandboxed iframe.

This isolates generated content from the main application.

The viewer therefore provides a controlled environment for displaying generated artifacts without granting unrestricted access to the parent page.

---

# 11. Streaming Implementation

## Requirement

The application needed to provide a responsive conversational experience rather than waiting for a complete model response.

## Implementation

Server-Sent Events were used for streaming.

The backend emits:

```text
token
sources
done
```

events.

The frontend progressively renders token events and then displays the retrieved source information after generation.

## Result

The user can see the response being generated progressively.

---

# 12. Persistence Correction

## Requirement

Conversation sessions must be independent and persisted.

## Implementation

Each chat receives a unique session ID.

Conversations and messages are stored in PostgreSQL.

The implementation stores:

* Session ID.
* Conversation metadata.
* Message role.
* Message content.
* Creation timestamps.
* Update timestamps.

## Result

Users can continue conversations and retrieve previous conversations from the application history.

---

# 13. Testing & Corrections

The backend was repeatedly tested after significant changes.

The final automated backend test run completed successfully with:

```text
23 passed
```

The Pi Agent integration also received dedicated tests.

Manual UI testing was used to verify the browser-level flows that are difficult to fully validate through backend unit tests, including:

* Streaming.
* Source display.
* Conversation history.
* Provider selection.
* Pi Agent mode.
* Artifact Viewer.
* Error states.

---

# 14. Final Agent Architecture

The final Growth Assistant flow is:

```text
User Question
      |
      v
Conversation History
      |
      v
Retrieval Query Construction
      |
      v
Ollama Embedding
      |
      v
PostgreSQL + pgvector
      |
      v
Relevant Transcript Chunks
      |
      v
Grounded Context
      |
      v
Pi Coding Agent
      |
      v
Ollama llama3.2:3b
      |
      v
Streaming Response
      |
      +---- Sources
      |
      v
Conversation Persistence
      |
      v
React UI
```

The key correction throughout development was to keep the **agent responsible for generation while the application remains responsible for retrieval, grounding, persistence, and source tracing**.

This separation makes the system easier to reason about, test, and operate locally.
