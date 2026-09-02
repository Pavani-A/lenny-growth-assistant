# Lenny Growth Assistant — Design Specification

## Figma Design

**Figma:** [Lenny Growth Assistant — UI Design]
(https://www.figma.com/design/1guHlCnfU9QKvzuiBaRrT2/Lenny-Growth-Assistant-%E2%80%94-UI-Design?node-id=0-1&t=AYgwLZnDvUYJnLCa-1)

The Figma file contains the visual design and primary UI states for the application, including:

- `01 — Main Chat`
- `02 — Grounded Answer`
- `03 — Not Enough Information`

---
## 1. Design Overview

The Lenny Growth Assistant uses a clean, minimal conversational interface designed to make grounded AI responses easy to understand and trust.

The design prioritizes:

- Clear conversation hierarchy.
- Visible grounding and source information.
- Simple interaction patterns.
- Minimal visual distraction.
- Easy access to generated artifacts.
- Clear handling of unsupported questions.

The UI is designed around the principle:

> **Make the answer easy to read and the source easy to trust.**

---

# 2. Design Goals

The interface should:

1. Make starting a conversation simple.
2. Keep the user's question and assistant response visually distinct.
3. Make grounded answers clearly identifiable.
4. Make supporting sources easy to find.
5. Clearly communicate when information is unavailable.
6. Support follow-up conversations naturally.
7. Provide a side-by-side Artifact Viewer.
8. Keep the interface clean and focused.

---

# 3. Information Architecture

The application is organized into two primary areas:

```text
┌─────────────────────────────────────────────────────┐
│ Sidebar                 │ Main Chat                 │
│                         │                           │
│ New Chat                │ Conversation              │
│                         │                           │
│ Previous Sessions       │ User Question             │
│                         │ Assistant Response        │
│                         │ Source                    │
│                         │                           │
│ Provider / Model        │                           │
└─────────────────────────────────────────────────────┘