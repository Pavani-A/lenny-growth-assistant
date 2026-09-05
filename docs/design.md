
# Lenny Growth Assistant — Design Specification

## Figma Design

**Figma:** [Lenny Growth Assistant — UI Design](https://www.figma.com/design/1guHlCnfU9QKvzuiBaRrT2/Lenny-Growth-Assistant-%E2%80%94-UI-Design?node-id=0-1&t=AYgwLZnDvUYJnLCa-1)

The Figma file contains the visual design and primary UI states for the application, including:

- `01 — Main Chat`
- `02 — Grounded Answer`
- `03 — Not Enough Information`

---

## 1. Design Overview

The Lenny Growth Assistant uses a clean, minimal conversational interface designed to make grounded AI responses easy to understand and trust.

The implemented UI prioritizes:

- Clear conversation hierarchy
- Visible grounding and source information
- Simple interaction patterns
- Minimal visual distraction
- Easy access to generated artifacts
- Clear handling of unsupported questions
- Persistent conversation history
- Explicit LLM provider selection
- Pi Agent mode

The UI is designed around the principle:

> **Make the answer easy to read and the source easy to trust.**

---

## 2. Design Goals

The interface should:

1. Make starting a conversation simple.
2. Keep the user's question and assistant response visually distinct.
3. Make grounded answers clearly identifiable.
4. Make supporting sources easy to find.
5. Clearly communicate when information is unavailable.
6. Support follow-up conversations naturally.
7. Provide an Artifact Viewer alongside the conversation.
8. Allow users to select their preferred LLM provider.
9. Provide a clear Pi Coding Agent mode.
10. Keep the interface clean and focused.

---

## 3. Information Architecture

The application is organized into two primary areas:

```text
┌──────────────────────────────────────────────────────────────┐
│ Sidebar                    │ Main Chat                       │
│                            │                                 │
│ New Chat                   │ Conversation                   │
│                            │                                 │
│ Previous Sessions          │ User Question                  │
│                            │ Assistant Response              │
│                            │                                 │
│ Provider Selector          │ Sources                         │
│ Pi Agent Toggle            │                                 │
│                            │ Artifact Viewer                 │
└──────────────────────────────────────────────────────────────┘
````

### Sidebar

The sidebar provides access to:

* New conversation
* Previous conversations
* Provider selection
* Pi Agent mode

The conversation history allows users to return to previously created sessions.

### Main Chat Area

The main area contains:

* User messages
* Assistant responses
* Streaming responses
* Retrieved transcript sources
* Artifact generation/viewing controls

---

## 4. Conversation Experience

### New Conversation

When the user starts a new chat, the frontend generates a new session ID.

The session is independent from previous conversations.

The user can immediately enter a product or growth question.

### Existing Conversation

Selecting a previous conversation loads its persisted messages.

The conversation can then continue from the existing session.

### Follow-up Questions

Follow-up questions use the existing session context.

For example:

```text
User:
What did successful product leaders say about onboarding?

Assistant:
[Grounded answer with sources]

User:
What about measuring onboarding success?

Assistant:
[Follow-up answer using the conversation context
and newly retrieved transcript evidence]
```

Previous assistant responses are used for conversational context but are not treated as factual evidence.

Transcript retrieval remains the source of truth.

---

## 5. Chat Message Design

User and assistant messages are visually differentiated.

The conversation follows a simple hierarchy:

```text
User Question
      ↓
Assistant Response
      ↓
Supporting Sources
```

Assistant responses are displayed progressively when streaming is enabled.

This allows the user to begin reading before the complete response has been generated.

---

## 6. Grounded Answer Design

Grounded responses should communicate both the answer and its supporting evidence.

The source section provides information such as:

* Episode title
* Guest
* Published date
* Transcript content
* Source URL
* YouTube URL

The design intentionally keeps source information accessible without overwhelming the main answer.

The user should be able to understand:

```text
Answer
  ↓
Why this answer is grounded
  ↓
Relevant transcript source
```

---

## 7. Unsupported / Insufficient Information State

The assistant is designed to acknowledge when the available transcript material does not contain enough evidence.

Instead of inventing an answer, the interface communicates that the available Lenny Podcast material is insufficient.

Example:

```text
┌──────────────────────────────────────────────┐
│ Assistant                                    │
│                                              │
│ I couldn't find enough relevant material     │
│ in the available Lenny Podcast transcripts   │
│ to answer this.                              │
└──────────────────────────────────────────────┘
```

This state reinforces the grounding principle and prevents unsupported claims from appearing as factual answers.

---

## 8. LLM Provider Selection

The interface provides an explicit provider selector with:

* Ollama
* Claude
* OpenAI

The selected provider is visible in the UI and is used for the corresponding chat request.

There is no automatic provider fallback.

If Claude or OpenAI is selected without the required configuration, the UI displays a clear configuration error.

For the local demo, Ollama is used.

---

## 9. Pi Agent Mode

The interface includes a Pi Agent toggle for the Growth Assistant experience.

When enabled:

* Pi Coding Agent is used.
* Ollama is used as the local model provider.
* The normal provider selector is disabled.
* The user can continue using the normal conversation experience.
* Transcript retrieval remains responsible for factual grounding.

The mode is intended to make the agent-based architecture visible and easy to demonstrate.

---

## 10. Source Display

Sources are displayed after the assistant response.

The source information allows users to inspect the transcript material that was retrieved for the answer.

A source can include:

```text
Episode
Guest
Published Date
Transcript Section
Source / YouTube Link
```

Multiple relevant transcript chunks can be displayed when they contribute to the answer.

The UI does not replace the transcript evidence with a generic citation label; the retrieved content remains available for inspection.

---

## 11. Artifact Viewer

The application provides an Artifact Viewer for generated content.

Supported artifact types include:

* Markdown
* HTML/CSS

The intended layout is:

```text
┌───────────────────────────┬────────────────────────────┐
│                           │                            │
│        Chat               │      Artifact Viewer       │
│                           │                            │
│ User Request              │      Generated Output      │
│                           │                            │
│ Assistant Response        │      Markdown / HTML       │
│                           │                            │
└───────────────────────────┴────────────────────────────┘
```

The viewer allows users to inspect generated artifacts without leaving the conversation.

### HTML Artifact Isolation

Generated HTML is treated as untrusted content.

HTML artifacts are rendered using a sandboxed iframe so generated content is isolated from the main application.

---

## 12. Ship 30 for 30 Experience

The application supports a dedicated Ship 30 for 30 generation flow.

The user can request newsletter-style content based on relevant Lenny transcript material.

The generated content is designed to include:

* Strong hook
* Narrative structure
* Clear headings
* Skimmable sections
* Bullets
* Bold emphasis
* Useful takeaway
* Transcript-grounded claims

The target length is approximately 1,250 words.

The resulting content can be presented as an artifact for further inspection.

---

## 13. Streaming Interaction

Chat responses use Server-Sent Events (SSE).

The UI receives:

```text
token
   ↓
token
   ↓
token
   ↓
...
   ↓
sources
   ↓
done
```

The interface renders the assistant response incrementally.

Once generation completes, the relevant source information is displayed.

This makes the interaction feel responsive while preserving source visibility.

---

## 14. Conversation History

The sidebar provides access to persisted conversations.

Each conversation is associated with a unique session ID.

The history experience allows the user to:

* Start a new chat
* View previous conversations
* Select a previous session
* Continue an existing conversation

Conversation messages are persisted by the backend in PostgreSQL.

---

## 15. Error States

The interface provides clear feedback for common failures.

### Empty Input

The user cannot submit an empty message.

### Missing Cloud Provider Configuration

When Claude or OpenAI is selected without the required API key, the UI displays a configuration message.

### Ollama Failure

If Ollama is unavailable, the selected request fails with an error rather than silently switching providers.

### Insufficient Retrieval

When the transcript knowledge base does not provide enough relevant evidence, the assistant communicates this explicitly.

### Artifact Generation Failure

If artifact generation fails, the UI reports the failure instead of presenting incomplete output as a successful artifact.

---

## 16. Visual Design Principles

The interface follows these principles:

### Clarity

Important information such as the user's question, assistant response, and sources should be visually distinguishable.

### Trust

Grounding information should be easy to access and inspect.

### Focus

The interface should avoid unnecessary visual elements that distract from the conversation.

### Responsiveness

Streaming responses should appear progressively.

### Discoverability

Core functionality such as provider selection, Pi Agent mode, conversation history, and artifact viewing should be easy to find.

### Safety

Generated HTML should remain isolated from the main application.

---

## 17. Implemented User Flow

The primary user journey is:

```text
Open Application
       |
       v
Start New Chat
       |
       v
Select Provider
       |
       v
Ask Product / Growth Question
       |
       v
Retrieve Relevant Transcript Chunks
       |
       v
Generate Grounded Response
       |
       v
Stream Response
       |
       v
Display Sources
       |
       v
Ask Follow-up
       |
       v
Conversation Context + New Retrieval
       |
       v
Continue Conversation
       |
       v
Generate Artifact if Required
       |
       v
View Artifact
```

---

## 18. Design-to-Implementation Mapping

| Design Element       | Implementation                               |
| -------------------- | -------------------------------------------- |
| Chat UI              | React + Vite                                 |
| Conversation history | PostgreSQL-backed conversation API           |
| Provider selector    | Ollama / Claude / OpenAI                     |
| Pi Agent toggle      | Pi Coding Agent + Ollama                     |
| Grounded responses   | Transcript retrieval + grounded agent        |
| Source display       | Retrieved transcript metadata and content    |
| Streaming            | Server-Sent Events                           |
| Artifact generation  | FastAPI artifact API                         |
| Artifact Viewer      | Sandboxed iframe                             |
| Persistent sessions  | PostgreSQL                                   |
| Error states         | Backend validation + frontend error handling |

The implemented design therefore reflects the current application architecture while keeping the core interface focused on grounded conversational assistance.


---

# 19. Design Decisions & Trade-offs

## 19.1 Conversation-First Layout

### Decision

The primary interface is organized around the conversation rather than exposing implementation details.

### Reason

The main user goal is to ask a product or growth question and understand the answer quickly.

Technical details such as retrieval, embeddings, and provider configuration should not dominate the main interaction.

---

## 19.2 Visible Sources

### Decision

Supporting transcript sources are displayed alongside grounded answers.

### Reason

The assistant is intentionally designed around trust and grounded responses.

Showing the episode, guest, transcript section, and source links allows the user to inspect the evidence behind an answer.

### Trade-off

Displaying source information adds visual complexity, but this is considered worthwhile because source transparency is a core product requirement.

---

## 19.3 Explicit Provider Selection

### Decision

The user explicitly selects Ollama, Claude, or OpenAI.

### Reason

Explicit selection makes provider behavior predictable and makes the architecture easy to demonstrate.

### Trade-off

The user has to understand which provider they are selecting instead of the application automatically choosing one.

Automatic fallback was intentionally avoided because it could hide configuration problems and make failures difficult to diagnose.

---

## 19.4 Pi Agent as a Separate Mode

### Decision

Pi Coding Agent is exposed through a dedicated toggle rather than replacing the normal chat flow.

### Reason

This makes the agent-based architecture visible while preserving a simple default conversational experience.

When Pi mode is enabled, Ollama is used for the local demonstration and the normal provider selector is disabled.

---

## 19.5 Sandboxed Artifact Viewer

### Decision

Generated HTML/CSS is rendered inside a sandboxed iframe.

### Reason

Generated HTML is untrusted content and should not have unrestricted access to the parent application.

### Trade-off

The sandbox introduces some browser restrictions, but the isolation is preferable to directly injecting generated HTML into the main application.

---

## 19.6 Streaming Responses

### Decision

Assistant responses are streamed using Server-Sent Events.

### Reason

Streaming allows users to start reading the response before generation has completely finished.

### Trade-off

Streaming introduces additional frontend and backend state handling compared with a single request/response operation, but it provides a more responsive conversational experience.

---

## 19.7 Sidebar + Main Content Structure

### Decision

The application uses a sidebar for navigation and controls, with the main area dedicated to the active conversation and artifacts.

### Reason

This separates persistent navigation and configuration from the primary conversational task.

The structure also makes conversation history easy to access without taking attention away from the current response.

---

## 19.8 Minimal Visual Design

### Decision

The interface intentionally uses a clean and minimal visual style.

### Reason

The product is information-heavy. Excessive decoration could make long AI responses, sources, and generated artifacts harder to scan.

The visual system therefore prioritizes hierarchy, readability, source visibility, and interaction clarity over decorative elements.

---

## 19.9 Responsive Behavior

### Decision

The interface prioritizes common desktop viewport sizes while keeping the core interaction usable across smaller viewport widths.

### Reason

The assignment's primary evaluation is a web application demonstration, so the design prioritizes the desktop conversational workflow while avoiding layouts that depend on a single fixed viewport.

---

## 19.10 Accessibility

### Decision

Interactive controls use clear labels and the interface maintains readable typography and visual hierarchy.

### Reason

The assistant contains several controls—including provider selection, Pi Agent mode, conversation history, chat input, and artifact interactions—so controls must remain understandable and discoverable.

Keyboard accessibility and clear interaction feedback are considered part of the design rather than optional enhancements.