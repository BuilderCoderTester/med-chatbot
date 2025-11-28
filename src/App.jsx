// src/App.jsx
import React, { useState, useEffect, useRef } from "react";

const BACKEND_URL = "http://localhost:8000/chat"; // Flask backend

export default function App() {
  const [conversations, setConversations] = useState([
    { id: "conv-1", title: "New chat", messages: [] },
  ]);
  const [currentId, setCurrentId] = useState("conv-1");
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState(null);

  const currentConversation = conversations.find((c) => c.id === currentId);

  const handleNewChat = () => {
    const newId = `conv-${Date.now()}`;
    const newConv = { id: newId, title: "New chat", messages: [] };
    setConversations((prev) => [newConv, ...prev]);
    setCurrentId(newId);
    setError(null);
  };

  const handleSelectConversation = (id) => {
    setCurrentId(id);
    setError(null);
  };

  const updateConversationMessages = (convId, updater) => {
    setConversations((prev) =>
      prev.map((c) =>
        c.id === convId ? { ...c, messages: updater(c.messages) } : c
      )
    );
  };

  const generateTitleFromFirstMessage = (text) => {
    if (!text) return "New chat";
    const trimmed = text.trim();
    return trimmed.length <= 30 ? trimmed : trimmed.slice(0, 27) + "...";
  };

  const handleSend = async () => {
    const question = input.trim();
    if (!question || !currentConversation || isSending) return;

    setIsSending(true);
    setInput("");
    setError(null);

    const timestamp = new Date().toLocaleTimeString();

    // 1) user message
    const userMsg = {
      id: `msg-${Date.now()}-user`,
      role: "user",
      content: question,
      timestamp,
    };
    updateConversationMessages(currentConversation.id, (msgs) => [
      ...msgs,
      userMsg,
    ]);

    // 2) auto title
    setConversations((prev) =>
      prev.map((c) =>
        c.id === currentConversation.id && c.title === "New chat"
          ? { ...c, title: generateTitleFromFirstMessage(question) }
          : c
      )
    );

    // 3) temp thinking message
    const thinkingId = `msg-${Date.now()}-assistant-pending`;
    const thinkingMsg = {
      id: thinkingId,
      role: "assistant",
      content: "Thinking...",
      pending: true,
      timestamp,
    };
    updateConversationMessages(currentConversation.id, (msgs) => [
      ...msgs,
      thinkingMsg,
    ]);

    try {
      const answerText = await callBackend(question);

      updateConversationMessages(currentConversation.id, (msgs) =>
        msgs.map((m) =>
          m.id === thinkingId
            ? {
                ...m,
                pending: false,
                content:
                  answerText ||
                  "I’m sorry, I couldn’t generate an answer right now.",
              }
            : m
        )
      );
    } catch (e) {
      console.error(e);
      setError("Something went wrong while talking to the medical assistant.");
      updateConversationMessages(currentConversation.id, (msgs) =>
        msgs.map((m) =>
          m.id === thinkingId
            ? {
                ...m,
                pending: false,
                content:
                  "⚠️ Error contacting server. Please try again in a moment.",
              }
            : m
        )
      );
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="app-root">
      <Sidebar
        conversations={conversations}
        currentId={currentId}
        onSelect={handleSelectConversation}
        onNewChat={handleNewChat}
      />

      <main className="main-panel">
        <Header />
        <section className="chat-section">
          {currentConversation ? (
            <>
              <ConversationSelector
                conversations={conversations}
                currentId={currentId}
                onSelect={handleSelectConversation}
              />

              <MessagesList messages={currentConversation.messages} />

              {error && <div className="error-banner">{error}</div>}

              <ChatInput
                value={input}
                onChange={setInput}
                onSend={handleSend}
                isSending={isSending}
                onKeyDown={handleKeyDown}
              />
            </>
          ) : (
            <div className="empty-state">
              <p>Select or create a conversation to begin.</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

async function callBackend(question) {
  const res = await fetch(BACKEND_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  const data = await res.json();
  return data.answer || data.response || "";
}

/* -------- Sidebar -------- */

function Sidebar({ conversations, currentId, onSelect, onNewChat }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1 className="logo">MedAI</h1>
        <button className="new-chat-btn" onClick={onNewChat}>
          + New chat
        </button>
      </div>
      <div className="sidebar-list">
        {conversations.length === 0 && (
          <div className="sidebar-empty">No conversations yet.</div>
        )}
        {conversations.map((conv) => (
          <button
            key={conv.id}
            className={
              "sidebar-item" +
              (conv.id === currentId ? " sidebar-item-active" : "")
            }
            onClick={() => onSelect(conv.id)}
          >
            <div className="sidebar-item-title">{conv.title}</div>
            <div className="sidebar-item-sub">
              {conv.messages.length} message
              {conv.messages.length === 1 ? "" : "s"}
            </div>
          </button>
        ))}
      </div>
      <div className="sidebar-footer">
        <span className="sidebar-footer-text">
          ⚕️ Educational only — not a replacement for a doctor.
        </span>
      </div>
    </aside>
  );
}

/* -------- Header -------- */

function Header() {
  return (
    <header className="header">
      <div>
        <h2 className="header-title">Medical Assistant</h2>
        <p className="header-subtitle">
          Ask medical questions based on your uploaded documents.
        </p>
      </div>
    </header>
  );
}

/* -------- Conversation Dropdown -------- */

function ConversationSelector({ conversations, currentId, onSelect }) {
  return (
    <div className="conv-dropdown-container">
      <select
        className="conv-dropdown"
        value={currentId}
        onChange={(e) => onSelect(e.target.value)}
      >
        {conversations.map((c) => (
          <option key={c.id} value={c.id}>
            {c.title}
          </option>
        ))}
      </select>
    </div>
  );
}

/* -------- Messages + Auto Scroll -------- */

function MessagesList({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    // scroll to bottom whenever number of messages changes
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages.length]);

  return (
    <div className="messages-list">
      {messages.length === 0 && (
        <div className="chat-empty">
          <p>Start by asking something like:</p>
          <ul>
            <li>“What is Acromegaly and gigantism?”</li>
            <li>“What is the treatment of acne?”</li>
            <li>“How is pneumonia diagnosed?”</li>
          </ul>
        </div>
      )}

      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}

      {/* anchor for auto-scroll */}
      <div ref={bottomRef} />
    </div>
  );
}

/* -------- Message Bubble -------- */

function MessageBubble({ message }) {
  const isUser = message.role === "user";
  return (
    <div
      className={`message-row ${
        isUser ? "message-row-user" : "message-row-assistant"
      }`}
    >
      <div className={`avatar ${isUser ? "avatar-user" : "avatar-assistant"}`}>
        {isUser ? "You" : "AI"}
      </div>
      <div className="bubble-wrapper">
        <div
          className={`bubble ${isUser ? "bubble-user" : "bubble-assistant"}`}
        >
          <p className="bubble-text">{message.content}</p>
          {message.pending && <TypingDots />}
        </div>
        <span className="bubble-meta">{message.timestamp}</span>
      </div>
    </div>
  );
}

/* -------- Typing Indicator -------- */

function TypingDots() {
  return (
    <span className="typing-dots">
      <span />
      <span />
      <span />
    </span>
  );
}

/* -------- Chat Input -------- */

function ChatInput({ value, onChange, onSend, isSending, onKeyDown }) {
  return (
    <div className="chat-input-container">
      <textarea
        className="chat-input"
        placeholder="Ask a medical question..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={onKeyDown}
        rows={2}
      />
      <button
        className="send-btn"
        onClick={onSend}
        disabled={!value.trim() || isSending}
      >
        {isSending ? "Sending..." : "Send"}
      </button>
    </div>
  );
}
