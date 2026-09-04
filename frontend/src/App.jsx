import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE_URL = "http://localhost:8000";

function createSessionId() {
  return crypto.randomUUID();
}

function getConversationGroup(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();

  const startOfToday = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate()
  );

  const startOfYesterday = new Date(startOfToday);
  startOfYesterday.setDate(startOfYesterday.getDate() - 1);

  const startOfSevenDaysAgo = new Date(startOfToday);
  startOfSevenDaysAgo.setDate(startOfSevenDaysAgo.getDate() - 7);

  if (date >= startOfToday) {
    return "Today";
  }

  if (date >= startOfYesterday) {
    return "Yesterday";
  }

  if (date >= startOfSevenDaysAgo) {
    return "Previous 7 days";
  }

  return "Older";
}

function App() {
  const [provider, setProvider] = useState("ollama");

  const [artifactOpen, setArtifactOpen] = useState(true);
  const [artifactWidth, setArtifactWidth] = useState(32);

  const [sessionId, setSessionId] = useState(createSessionId());

  const [conversations, setConversations] = useState([]);
  const [messages, setMessages] = useState([]);

  const [messageInput, setMessageInput] = useState("");

  const [loadingHistory, setLoadingHistory] = useState(false);
  const [loadingConversation, setLoadingConversation] = useState(false);
  const [sending, setSending] = useState(false);

  const [error, setError] = useState("");

  const [conversationTitle, setConversationTitle] =
    useState("New conversation");

  // Artifact state
  const [artifact, setArtifact] = useState(null);
  const [artifactLoading, setArtifactLoading] = useState(false);
  const [artifactError, setArtifactError] = useState("");

  const handleDividerDrag = (clientX, container) => {
  const rect = container.getBoundingClientRect();

  const newWidth =
    ((rect.right - clientX) / rect.width) * 100;

  const clampedWidth = Math.min(
    Math.max(newWidth, 25),
    70
  );

  setArtifactWidth(clampedWidth);
};

const startDragging = (event) => {
  event.preventDefault();

  // Capture the container immediately while the React event is valid.
  const container = event.currentTarget.parentElement;

  const handleMove = (moveEvent) => {
    handleDividerDrag(
      moveEvent.clientX,
      container
    );
  };

  const stopDragging = () => {
    window.removeEventListener(
      "pointermove",
      handleMove
    );

    window.removeEventListener(
      "pointerup",
      stopDragging
    );
  };

  window.addEventListener(
    "pointermove",
    handleMove
  );

  window.addEventListener(
    "pointerup",
    stopDragging
  );
};

  const loadConversations = async () => {
    try {
      setLoadingHistory(true);

      const response = await fetch(
        `${API_BASE_URL}/api/v1/conversations`
      );

      if (!response.ok) {
        throw new Error(
          "Unable to load conversation history."
        );
      }

      const data = await response.json();

      setConversations(data);
    } catch (err) {
      console.error(err);
      setError("Could not load conversation history.");
    } finally {
      setLoadingHistory(false);
    }
  };

  const loadConversation = async (selectedSessionId) => {
    try {
      setLoadingConversation(true);
      setError("");

      setArtifact(null);
      setArtifactError("");

      const response = await fetch(
        `${API_BASE_URL}/api/v1/conversations/${encodeURIComponent(
          selectedSessionId
        )}`
      );

      if (!response.ok) {
        throw new Error("Unable to load conversation.");
      }

      const data = await response.json();

      setSessionId(data.session_id);
      setMessages(data.messages || []);

      const selectedConversation = conversations.find(
        (conversation) =>
          conversation.session_id === selectedSessionId
      );

      setConversationTitle(
        selectedConversation?.title || "Conversation"
      );
    } catch (err) {
      console.error(err);
      setError("Could not load this conversation.");
    } finally {
      setLoadingConversation(false);
    }
  };

  const startNewChat = () => {
    setSessionId(createSessionId());
    setMessages([]);
    setMessageInput("");
    setConversationTitle("New conversation");
    setError("");

    setArtifact(null);
    setArtifactError("");
  };

  const sendMessage = async () => {
    const message = messageInput.trim();

    if (!message || sending) {
      return;
    }

    setError("");
    setSending(true);

    const userMessage = {
      role: "user",
      content: message,
      created_at: new Date().toISOString(),
    };

    const assistantMessage = {
      role: "assistant",
      content: "",
      created_at: new Date().toISOString(),
      sources: [],
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
      assistantMessage,
    ]);

    setMessageInput("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/chat/stream`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message,
            session_id: sessionId,
            provider,
          }),
        }
      );

      if (!response.ok) {
        let errorMessage =
          "The assistant could not process your request.";

        try {
          const data = await response.json();

          errorMessage =
            data?.detail?.message || errorMessage;
        } catch {
          // Keep the default error message.
        }

        throw new Error(errorMessage);
      }

      if (!response.body) {
        throw new Error(
          "The server did not return a streaming response."
        );
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = "";

      const appendAssistantContent = (content) => {
        if (!content) {
          return;
        }

        setMessages((currentMessages) => {
          const updatedMessages = [...currentMessages];

          for (
            let index = updatedMessages.length - 1;
            index >= 0;
            index -= 1
          ) {
            if (
              updatedMessages[index].role ===
              "assistant"
            ) {
              updatedMessages[index] = {
                ...updatedMessages[index],
                content:
                  updatedMessages[index].content +
                  content,
              };

              break;
            }
          }

          return updatedMessages;
        });
      };

      const setAssistantSources = (sources) => {
        setMessages((currentMessages) => {
          const updatedMessages = [...currentMessages];

          for (
            let index = updatedMessages.length - 1;
            index >= 0;
            index -= 1
          ) {
            if (
              updatedMessages[index].role ===
              "assistant"
            ) {
              updatedMessages[index] = {
                ...updatedMessages[index],
                sources: sources || [],
              };

              break;
            }
          }

          return updatedMessages;
        });
      };

      const processEvent = (eventText) => {
        const lines = eventText.split("\n");

        let eventName = "";
        let data = "";

        for (const line of lines) {
          if (line.startsWith("event:")) {
            eventName = line.slice(6).trim();
          }

          if (line.startsWith("data:")) {
            data += line.slice(5).trim();
          }
        }

        if (!eventName || !data) {
          return;
        }

        try {
          const parsedData = JSON.parse(data);

          if (eventName === "token") {
            appendAssistantContent(
              parsedData.content || ""
            );
          }

          if (eventName === "sources") {
            setAssistantSources(
              parsedData.sources || []
            );
          }
        } catch (parseError) {
          console.error(
            "Could not parse SSE event:",
            parseError
          );
        }
      };

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          buffer += decoder.decode();
          break;
        }

        buffer += decoder.decode(value, {
          stream: true,
        });

        const events = buffer.split("\n\n");

        buffer = events.pop() || "";

        for (const event of events) {
          processEvent(event);
        }
      }

      if (buffer.trim()) {
        processEvent(buffer);
      }

      if (conversationTitle === "New conversation") {
        setConversationTitle(
          message.length > 45
            ? `${message.slice(0, 42).trim()}...`
            : message
        );
      }

      await loadConversations();
    } catch (err) {
      console.error(err);

      setError(err.message);

      setMessages((currentMessages) => {
        const updatedMessages = [...currentMessages];

        const lastMessage =
          updatedMessages[updatedMessages.length - 1];

        if (
          lastMessage?.role === "assistant" &&
          lastMessage?.content === ""
        ) {
          updatedMessages.pop();
        }

        return updatedMessages;
      });
    } finally {
      setSending(false);
    }
  };

  const handleComposerKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  /*
   * Generate an artifact from the current conversation.
   *
   * The backend contract is:
   *
   * POST /api/v1/artifacts
   *
   * {
   *   prompt,
   *   session_id,
   *   provider
   * }
   *
   * Response:
   *
   * {
   *   session_id,
   *   provider,
   *   artifact: {
   *     type,
   *     title,
   *     content
   *   }
   * }
   */
  const createArtifact = async () => {
    if (artifactLoading) {
      return;
    }

    if (messages.length === 0) {
      setArtifactError(
        "Start a conversation before creating an artifact."
      );
      return;
    }

    setArtifactLoading(true);
    setArtifactError("");
    setArtifactOpen(true);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/artifacts`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            prompt:
              "Create a useful product or growth artifact based on the current conversation. Use the conversation context to determine the most useful artifact. Prefer a complete HTML artifact when a visual presentation is useful. Make it clear, practical, skimmable, and grounded in the transcript-based discussion.",
            session_id: sessionId,
            provider,
          }),
        }
      );

      let data;

      try {
        data = await response.json();
      } catch {
        throw new Error(
          "The artifact service returned an invalid response."
        );
      }

      if (!response.ok) {
        throw new Error(
          data?.detail?.message ||
            "The artifact could not be generated."
        );
      }

      if (
        !data.artifact ||
        !data.artifact.type ||
        !data.artifact.title ||
        !data.artifact.content
      ) {
        throw new Error(
          "The server returned an incomplete artifact."
        );
      }

      setArtifact(data.artifact);
    } catch (err) {
      console.error(err);

      setArtifact(null);
      setArtifactError(err.message);
    } finally {
      setArtifactLoading(false);
    }
  };

  useEffect(() => {
    loadConversations();
  }, []);

  const groupedConversations = useMemo(() => {
    const groups = {
      Today: [],
      Yesterday: [],
      "Previous 7 days": [],
      Older: [],
    };

    conversations.forEach((conversation) => {
      const group = getConversationGroup(
        conversation.updated_at
      );

      groups[group].push(conversation);
    });

    return groups;
  }, [conversations]);

  const renderConversationGroup = (groupName) => {
    const group = groupedConversations[groupName];

    if (!group || group.length === 0) {
      return null;
    }

    return (
      <div key={groupName}>
        <div className="section-label">
          {groupName}
        </div>

        {group.map((conversation) => (
          <button
            key={conversation.session_id}
            className={`conversation ${
              conversation.session_id === sessionId
                ? "active"
                : ""
            }`}
            onClick={() =>
              loadConversation(conversation.session_id)
            }
            disabled={loadingConversation || sending}
          >
            <span>{conversation.title}</span>
          </button>
        ))}
      </div>
    );
  };

  return (
    <div className="app-shell">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-top">
          <div className="brand">
            <div className="brand-mark">L</div>

            <div>
              <h1>Lenny</h1>
              <span>Growth Assistant</span>
            </div>
          </div>

          <button
            className="new-chat-button"
            onClick={startNewChat}
            disabled={sending}
          >
            <span>+</span>
            New chat
          </button>

          <div className="conversation-section">
            {loadingHistory &&
            conversations.length === 0 ? (
              <div className="section-label">
                Loading conversations...
              </div>
            ) : (
              <>
                {renderConversationGroup("Today")}

                {renderConversationGroup("Yesterday")}

                {renderConversationGroup(
                  "Previous 7 days"
                )}

                {renderConversationGroup("Older")}
              </>
            )}
          </div>
        </div>

        <div className="sidebar-bottom">
          <button className="sidebar-item">
            <span>⚙</span>
            Settings
          </button>

          <button className="sidebar-item">
            <span>?</span>
            About
          </button>
        </div>
      </aside>

      {/* Main workspace */}
      <main className="workspace">
        {/* Chat */}
        <section
          className="chat-panel"
          style={{
            flex: artifactOpen
              ? `0 0 ${100 - artifactWidth}%`
              : "1",
          }}
        >
          <header className="chat-header">
            <div>
              <span className="eyebrow">
                CONVERSATION
              </span>

              <h2>{conversationTitle}</h2>
            </div>

            <div className="provider-control">
              <label htmlFor="provider">
                Model
              </label>

              <select
                id="provider"
                value={provider}
                onChange={(event) =>
                  setProvider(event.target.value)
                }
                disabled={sending}
              >
                <option value="ollama">
                  Ollama
                </option>

                <option value="claude">
                  Claude
                </option>

                <option value="openai">
                  OpenAI
                </option>
              </select>
            </div>
          </header>

          {/* Only this area scrolls */}
          <div className="messages">
            {messages.length === 0 &&
              !loadingConversation && (
                <div className="message assistant-message">
                  <div className="avatar">L</div>

                  <div className="message-content">
                    <div className="message-name">
                      Lenny Growth Assistant
                    </div>

                    <p>
                      Hi! I can help you think through
                      product and growth questions using
                      the available Lenny's Podcast
                      transcripts.
                    </p>
                  </div>
                </div>
              )}

            {loadingConversation && (
              <div className="message assistant-message">
                <div className="avatar">L</div>

                <div className="message-content">
                  <div className="message-name">
                    Lenny Growth Assistant
                  </div>

                  <p>Loading conversation...</p>
                </div>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                className={`message ${
                  message.role === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
                key={`${message.created_at}-${index}`}
              >
                {message.role === "assistant" && (
                  <div className="avatar">L</div>
                )}

                <div className="message-content">
                  {message.role === "assistant" && (
                    <div className="message-name">
                      Lenny Growth Assistant
                    </div>
                  )}

                  {message.content ? (
                    message.content
                      .split("\n\n")
                      .map(
                        (paragraph, paragraphIndex) => (
                          <p key={paragraphIndex}>
                            {paragraph}
                          </p>
                        )
                      )
                  ) : sending &&
                    index === messages.length - 1 ? (
                    <p>Thinking...</p>
                  ) : null}

                  {message.sources &&
                    message.sources.length > 0 && (
                      <div className="sources">
                        <div className="sources-title">
                          Sources
                        </div>

                        {message.sources.map(
                          (source, sourceIndex) => (
                            <div
                              className="source"
                              key={`${source.episode_title}-${source.chunk_index}-${sourceIndex}`}
                            >
                              <div>
                                <strong>
                                  Episode
                                </strong>

                                <span>
                                  {
                                    source.episode_title
                                  }
                                </span>
                              </div>

                              {source.guest && (
                                <div>
                                  <strong>
                                    Guest
                                  </strong>

                                  <span>
                                    {source.guest}
                                  </span>
                                </div>
                              )}

                              {source.published_date && (
                                <div>
                                  <strong>
                                    Published
                                  </strong>

                                  <span>
                                    {
                                      source.published_date
                                    }
                                  </span>
                                </div>
                              )}

                              {source.youtube_url && (
                                <div>
                                  <strong>
                                    Source Video
                                  </strong>

                                  <a
                                    href={
                                      source.youtube_url
                                    }
                                    target="_blank"
                                    rel="noreferrer"
                                  >
                                    Watch episode
                                  </a>
                                </div>
                              )}

                              {source.source_url && (
                                <div>
                                  <strong>
                                    Transcript Source
                                  </strong>

                                  <a
                                    href={
                                      source.source_url
                                    }
                                    target="_blank"
                                    rel="noreferrer"
                                  >
                                    View transcript
                                  </a>
                                </div>
                              )}

                              <details>
                                <summary>
                                  Relevant excerpt
                                </summary>

                                <p>
                                  {source.content}
                                </p>
                              </details>
                            </div>
                          )
                        )}
                      </div>
                    )}
                </div>
              </div>
            ))}

            {error && (
              <div className="message assistant-message">
                <div className="avatar">!</div>

                <div className="message-content">
                  <div className="message-name">
                    Something went wrong
                  </div>

                  <p>{error}</p>
                </div>
              </div>
            )}
          </div>

          {/* Fixed composer */}
          <div className="composer-area">
            <div className="composer">
              <textarea
                placeholder="Ask a product or growth question..."
                rows={1}
                value={messageInput}
                onChange={(event) =>
                  setMessageInput(event.target.value)
                }
                onKeyDown={handleComposerKeyDown}
                disabled={sending}
              />

              <div className="composer-footer">
                <span>
                  Grounded in Lenny's Podcast transcripts
                </span>

                <button
                  className="send-button"
                  onClick={sendMessage}
                  disabled={
                    sending ||
                    !messageInput.trim()
                  }
                  aria-label="Send message"
                >
                  ↑
                </button>
              </div>
            </div>

            <div className="composer-hint">
              AI can make mistakes. Check important
              information against the original sources.
            </div>
          </div>
        </section>

        {/* Artifact */}
        {artifactOpen && (
          <>
            <div
              className="resize-divider"
              onPointerDown={startDragging}
              role="separator"
              aria-label="Resize artifact panel"
              tabIndex={0}
            >
              <div className="resize-handle" />
            </div>

            <aside
              className="artifact-panel"
              style={{
                flex: `0 0 ${artifactWidth}%`,
              }}
            >
              <header className="artifact-header">
                <div>
                  <span className="eyebrow">
                    ARTIFACT
                  </span>

                  <h2>
                    {artifact?.title ||
                      "Artifact Viewer"}
                  </h2>
                </div>

                <button
                  className="close-artifact"
                  onClick={() =>
                    setArtifactOpen(false)
                  }
                  aria-label="Close artifact viewer"
                >
                  ×
                </button>
              </header>

              <div className="artifact-content">
                {/* Loading state */}
                {artifactLoading && (
                  <div className="artifact-placeholder">
                    <div className="artifact-icon">
                      ✦
                    </div>

                    <h3>
                      Generating artifact...
                    </h3>

                    <p>
                      Lenny is creating an artifact
                      from the current conversation.
                    </p>
                  </div>
                )}

                {/* Error state */}
                {!artifactLoading &&
                  artifactError && (
                    <div className="artifact-placeholder">
                      <div className="artifact-icon">
                        !
                      </div>

                      <h3>
                        Artifact generation failed
                      </h3>

                      <p>{artifactError}</p>

                      <button
                        className="create-artifact-button"
                        onClick={createArtifact}
                      >
                        Try again
                      </button>
                    </div>
                  )}

                {/* Empty state */}
                {!artifactLoading &&
                  !artifactError &&
                  !artifact && (
                    <div className="artifact-placeholder">
                      <div className="artifact-icon">
                        ✦
                      </div>

                      <h3>
                        Your artifact will appear
                        here
                      </h3>

                      <p>
                        Generate a checklist, framework,
                        comparison, dashboard, or other
                        visual artifact from the
                        conversation.
                      </p>

                      <button
                        className="create-artifact-button"
                        onClick={createArtifact}
                        disabled={messages.length === 0}
                      >
                        ✦ Create artifact
                      </button>
                    </div>
                  )}

                {/* Generated artifact */}
                {!artifactLoading &&
                  !artifactError &&
                  artifact && (
                    <div
                      className="generated-artifact"
                      style={{
                        height: "100%",
                      }}
                    >
                      {artifact.type === "html" ? (
                        <iframe
                          title={artifact.title}
                          srcDoc={artifact.content}
                          sandbox=""
                          style={{
                            width: "100%",
                            height: "100%",
                            minHeight: "600px",
                            border: "0",
                            background: "#ffffff",
                          }}
                        />
                      ) : (
                        <div
                          style={{
                            whiteSpace: "pre-wrap",
                            background: "#ffffff",
                            padding: "20px",
                            borderRadius: "8px",
                            minHeight: "100%",
                            fontFamily:
                              "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
                            fontSize: "12px",
                            lineHeight: "1.6",
                          }}
                        >
                          {artifact.content}
                        </div>
                      )}
                    </div>
                  )}
              </div>
            </aside>
          </>
        )}

        {/* Re-open artifact panel */}
        {!artifactOpen && (
          <button
            className="open-artifact-button"
            onClick={() => setArtifactOpen(true)}
          >
            ✦ Artifact
          </button>
        )}
      </main>
    </div>
  );
}

export default App;