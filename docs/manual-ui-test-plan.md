# Lenny Growth Assistant — Manual UI Test Plan

## 1. Purpose

This document defines the manual UI tests used to verify the main user flows of the Lenny Growth Assistant.

The tests focus on:

- Chat functionality
- Streaming responses
- Source grounding
- Conversation history
- Follow-up questions
- Unsupported questions
- LLM provider selection
- Pi Agent mode
- Ship 30 for 30 generation
- Artifact generation
- Artifact Viewer
- Error handling

---

## 2. Test Environment

### Frontend

- React
- Vite
- Local development server

### Backend

- FastAPI
- Local development server

### Database

- PostgreSQL
- pgvector
- Docker Compose

### Local LLM

- Ollama
- `llama3.2:3b`
- `embeddinggemma`

### Browser

Use a modern Chromium-based browser such as Chrome or Edge.

---

## 3. Preconditions

Before testing:

1. PostgreSQL is running through Docker Compose.
2. Ollama is running.
3. Required Ollama models are available.
4. Backend is running.
5. Frontend is running.
6. Transcript data has been ingested.
7. The application is accessible from the browser.

---

# 4. Test Cases

## TC-01 — Application Loads

**Objective:** Verify that the application loads successfully.

### Steps

1. Open the frontend URL.
2. Wait for the application to load.
3. Observe the main interface.

### Expected Result

- The application loads without a blank screen.
- The sidebar is visible.
- The chat interface is visible.
- Provider controls are visible.
- No unexpected error is displayed.

### Status

Pass / Fail

---

## TC-02 — Health Check

**Objective:** Verify that the backend is available.

### Steps

1. Open the backend health endpoint.
2. Inspect the response.

### Expected Result

The API returns a successful response indicating that the service is healthy.

### Status

Pass / Fail

---

## TC-03 — Start a New Chat

**Objective:** Verify that a new conversation can be started.

### Steps

1. Open the application.
2. Enter a product or growth question.
3. Submit the question.

### Expected Result

- The user message appears in the conversation.
- The assistant begins generating a response.
- The response is displayed in the chat.

### Status

Pass / Fail

---

## TC-04 — Streaming Response

**Objective:** Verify that responses are streamed progressively.

### Steps

1. Start a new chat.
2. Ask a question supported by the transcript data.
3. Observe the assistant response while it is being generated.

### Expected Result

- The response appears progressively rather than waiting for the entire answer.
- The UI remains responsive.
- The final response is displayed completely.

### Status

Pass / Fail

---

## TC-05 — Grounded Answer and Sources

**Objective:** Verify that supported questions produce transcript-grounded answers.

### Steps

1. Ask a question related to a topic covered by Lenny's Podcast.
2. Wait for the response.
3. Inspect the source section.

### Expected Result

- The assistant provides an answer based on retrieved transcript material.
- Supporting source information is displayed.
- Source information identifies the relevant episode or transcript content.

### Status

Pass / Fail

---

## TC-06 — Follow-Up Question

**Objective:** Verify that conversation context is preserved.

### Steps

1. Ask an initial question.
2. Wait for the answer.
3. Ask a follow-up question using a reference such as "What about that approach?"
4. Observe the response.

### Expected Result

- The assistant understands the follow-up in the context of the previous conversation.
- The response uses newly retrieved transcript evidence.
- The conversation remains in the same session.

### Status

Pass / Fail

---

## TC-07 — Conversation History

**Objective:** Verify that previous conversations are persisted and displayed.

### Steps

1. Start a conversation.
2. Ask at least one question.
3. Refresh the page.
4. Inspect the conversation sidebar/history.

### Expected Result

- The previous conversation remains available.
- The conversation can be selected.
- Previously stored messages can be viewed.

### Status

Pass / Fail

---

## TC-08 — Unsupported Question

**Objective:** Verify that the assistant does not confidently answer questions unsupported by the transcript data.

### Steps

1. Start a new conversation.
2. Ask a question that is unrelated to Lenny's Podcast transcript content.
3. Wait for the response.

### Expected Result

- The assistant communicates that the available transcript material does not provide enough evidence.
- It does not present unrelated external knowledge as transcript-grounded information.

### Status

Pass / Fail

---

## TC-09 — Ollama Provider

**Objective:** Verify the local Ollama provider.

### Steps

1. Select **Ollama** from the provider selector.
2. Ask a supported question.
3. Wait for the response.

### Expected Result

- The request is processed using Ollama.
- A response is generated successfully.
- No cloud API key is required.

### Status

Pass / Fail

---

## TC-10 — Cloud Provider Configuration Error

**Objective:** Verify that a missing cloud provider configuration is handled clearly.

### Steps

1. Select Claude or OpenAI.
2. Use an environment where the corresponding API key is not configured.
3. Submit a question.

### Expected Result

- The application does not silently switch to another provider.
- A clear configuration error is shown.
- The user is informed that the required API key must be configured.

### Status

Pass / Fail

---

## TC-11 — Pi Agent Mode

**Objective:** Verify the Pi Coding Agent flow.

### Steps

1. Enable the **Pi Agent** toggle.
2. Confirm that the provider selector reflects the Pi Agent configuration.
3. Ask a product or growth question.
4. Wait for the response.

### Expected Result

- Pi Agent mode is enabled.
- Ollama is used for the local Pi configuration.
- The Growth Assistant returns a response.
- The response remains grounded in retrieved transcript context.

### Status

Pass / Fail

---

## TC-12 — Pi Agent Follow-Up

**Objective:** Verify conversation persistence in Pi Agent mode.

### Steps

1. Enable Pi Agent mode.
2. Ask an initial question.
3. Ask a follow-up question referencing the previous answer.

### Expected Result

- The conversation remains in the same session.
- The follow-up is interpreted using previous conversation context.
- The assistant retrieves transcript evidence for the current question.

### Status

Pass / Fail

---

## TC-13 — Ship 30 for 30 Generation

**Objective:** Verify the Ship 30 for 30 content generation flow.

### Steps

1. Ask the assistant to create a Ship 30 for 30-style article about a supported product or growth topic.
2. Wait for generation to complete.
3. Inspect the generated content.

### Expected Result

The generated content should contain:

- A strong opening hook.
- Clear narrative structure.
- Headings.
- Skimmable sections.
- Useful takeaways.
- Transcript-grounded claims.

### Status

Pass / Fail

---

## TC-14 — Artifact Generation

**Objective:** Verify that an artifact can be generated.

### Steps

1. Ask the assistant to create an artifact.
2. Wait for generation.
3. Inspect the Artifact Viewer.

### Expected Result

- The artifact is generated successfully.
- The Artifact Viewer becomes available.
- The generated content is displayed separately from the conversation.

### Status

Pass / Fail

---

## TC-15 — Markdown Artifact

**Objective:** Verify Markdown artifact generation.

### Steps

1. Request a Markdown artifact.
2. Wait for generation.
3. Inspect the generated artifact.

### Expected Result

- Markdown content is generated.
- The content is readable and correctly structured.
- The artifact is displayed in the Artifact Viewer.

### Status

Pass / Fail

---

## TC-16 — HTML/CSS Artifact

**Objective:** Verify HTML/CSS artifact rendering.

### Steps

1. Request an HTML/CSS artifact.
2. Wait for generation.
3. Open the Artifact Viewer.

### Expected Result

- The generated HTML/CSS is rendered inside the viewer.
- The artifact does not replace or interfere with the main application UI.
- The artifact is isolated from the parent application.

### Status

Pass / Fail

---

## TC-17 — Artifact Isolation

**Objective:** Verify that generated HTML is isolated from the main application.

### Steps

1. Generate an HTML artifact.
2. Inspect the Artifact Viewer.
3. Interact with the artifact.
4. Observe the parent application.

### Expected Result

- The artifact is rendered inside the sandboxed viewer.
- The generated content does not gain unrestricted access to the parent application.
- The main application remains functional.

### Status

Pass / Fail

---

## TC-18 — Empty Message Validation

**Objective:** Verify client/server handling of invalid chat input.

### Steps

1. Leave the chat input empty.
2. Attempt to submit the message.

### Expected Result

- The application prevents an invalid empty request or displays a validation error.
- No empty assistant response is generated.

### Status

Pass / Fail

---

## TC-19 — Ollama Unavailable

**Objective:** Verify resilience when the local LLM is unavailable.

### Steps

1. Stop the Ollama service.
2. Select Ollama.
3. Submit a chat request.

### Expected Result

- The request does not appear successful.
- A clear error is displayed.
- The application does not crash or become unusable.

### Status

Pass / Fail

---

## TC-20 — Database Unavailable

**Objective:** Verify behavior when PostgreSQL is unavailable.

### Steps

1. Stop the PostgreSQL Docker container.
2. Attempt to load conversations or submit a request requiring persistence.

### Expected Result

- The application reports the database-related failure.
- The frontend remains usable enough to display the error.
- The backend process does not unexpectedly terminate.

### Status

Pass / Fail

---

# 5. Regression Checklist

Before the final demo, verify:

- [ ] Application loads.
- [ ] Backend health endpoint works.
- [ ] Ollama is available.
- [ ] Chat request works.
- [ ] Streaming works.
- [ ] Sources are displayed.
- [ ] Follow-up questions work.
- [ ] Conversation history persists.
- [ ] Unsupported questions are handled safely.
- [ ] Ollama provider works.
- [ ] Claude/OpenAI configuration errors are clear.
- [ ] Pi Agent mode works.
- [ ] Ship 30 for 30 generation works.
- [ ] Markdown artifact generation works.
- [ ] HTML/CSS artifact generation works.
- [ ] Artifact Viewer works.
- [ ] HTML artifact is sandboxed.
- [ ] Empty input validation works.
- [ ] Application handles Ollama failures.
- [ ] Application handles database failures.

---

# 6. Final Acceptance Criteria

The application is considered ready for demonstration when the evaluator can:

1. Open the application.
2. Start a conversation.
3. Ask a grounded product/growth question.
4. Observe a streamed answer.
5. Inspect supporting transcript sources.
6. Ask a contextual follow-up.
7. View the conversation in history.
8. Ask an unsupported question and observe a safe response.
9. Enable Pi Agent mode.
10. Generate Ship 30 for 30-style content.
11. Generate an artifact.
12. View the artifact inside the application.
13. Switch between supported providers or observe clear configuration errors when a provider is unavailable.