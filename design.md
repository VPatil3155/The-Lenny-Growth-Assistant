# 🎨 Design Document

## The Lenny Growth Assistant

---

# Table of Contents

1. UI Design
2. Application Layout
3. Component Architecture
4. State Management
5. API Flow
6. User Flow
7. Design Decisions
8. Responsive Design
9. Future Improvements

---

# 1. UI Design

The application follows a **minimal, modern dashboard layout** focused on productivity and readability. The interface is divided into two primary workflows:

- **AI Chat**
- **Artifact Generation**

The design emphasizes:

- Clean workspace
- Minimal distractions
- Fast navigation
- Responsive layouts
- Consistent spacing
- Markdown-friendly output

---

# 2. Application Layout

## Overall Layout

```text
+--------------------------------------------------------------+
| Header                                                       |
|--------------------------------------------------------------|
| Logo | Provider Selector | Chat | Artifacts                  |
+--------------------------------------------------------------+

                Page Content

+--------------------------------------------------------------+
|                                                              |
|               Current Page (Chat / Artifacts)                |
|                                                              |
+--------------------------------------------------------------+
```

---

## Chat Page

```text
+-------------+-----------------------------------------------+
|             |                                               |
|             |             Chat Window                       |
|             |                                               |
|  Sidebar    |  User Message                                 |
|             |                                               |
|  Sessions   |  Assistant Reply                              |
|             |                                               |
|             |                                               |
+-------------+-----------------------------------------------+
|                  Message Input + Send                        |
+-------------------------------------------------------------+
```

### Sidebar

- New Chat
- Session List
- Rename Session
- Delete Session

### Chat Window

Displays

- User messages
- Assistant messages
- Markdown responses
- Loading state

### Message Input

Supports

- Multi-line input
- Enter to Send
- Shift + Enter for new line

---

## Artifact Page

```text
+--------------------------+--------------------------------+
|                          |                                |
| Generate Artifact Form   |  Artifact Preview              |
|                          |                                |
| Type                     |  Markdown Viewer               |
| Topic                    |                                |
| Context                  |                                |
|                          |  Copy                          |
| Generate                 |  Download                      |
+--------------------------+--------------------------------+
```

The preview panel appears only after an artifact has been generated.

---

# 3. Component Architecture

```text
App

├── Header
│     └── ProviderSelector
│
├── Chat Page
│     ├── Sidebar
│     ├── ChatWindow
│     │      └── MessageBubble
│     └── MessageInput
│
└── Artifact Page
      ├── Artifact Form
      └── ArtifactPanel
             └── ArtifactViewer
```

---

# 4. State Management

The application uses **React Hooks**.

No global state library (Redux, Zustand, MobX) is required.

## useChat

Responsible for

- Sessions
- Active Chat
- Messages
- Sending state
- Loading state
- Errors

---

## useArtifact

Responsible for

- Artifact generation
- Loading state
- Error handling
- Clearing artifacts

---

## useProvider

Responsible for

- Current Provider
- Provider Switching
- Provider Availability

---

# 5. Backend Architecture

```text
Frontend

↓

REST API

↓

FastAPI

↓

Chat Orchestrator

↓

RAG Engine

↓

LLM Provider Factory

↓

OpenAI / Ollama
```

---

# 6. Chat Processing Flow

```text
User

↓

Send Message

↓

POST /sessions/{id}/messages

↓

Store User Message

↓

Load Conversation

↓

Retrieve Knowledge

↓

Build Prompt

↓

Selected LLM

↓

Assistant Response

↓

Save Response

↓

Return Response
```

---

# 7. Artifact Generation Flow

```text
User

↓

Generate Artifact

↓

Artifact Service

↓

Template Builder

↓

LLM

↓

Markdown Output

↓

Artifact Viewer
```

---

# 8. Provider Switching

```text
Provider Selector

↓

POST /provider

↓

Update Provider Factory

↓

Next Request Uses

OpenAI

or

Ollama
```

No backend restart is required.

---

# 9. Retrieval-Augmented Generation (RAG)

```text
Knowledge Files

↓

Document Loader

↓

Chunker

↓

Retriever

↓

Relevant Chunks

↓

Prompt Builder

↓

LLM
```

Current implementation

| Component | Description |
|------------|-------------|
| Loader | Reads Markdown documents |
| Chunker | Splits into overlapping chunks |
| Retriever | Keyword-based Top-3 retrieval |
| Prompt Builder | Combines system prompt, retrieved context, history, and current query |

---

# 10. Responsive Design

| Screen Size | Behavior |
|-------------|----------|
| Desktop | Sidebar + Main Panel |
| Tablet | Responsive Flex Layout |
| Mobile | Full-width Panels |

The artifact panel automatically becomes a full-screen overlay on smaller devices.

---

# 11. Error Handling

Frontend

- Loading indicators
- Error messages
- Disabled buttons while processing

Backend

- Validation
- HTTP Exceptions
- Provider availability checks
- Database error handling

---

# 12. Design Decisions

| Decision | Reason |
|-----------|--------|
| FastAPI | Lightweight, fast, async support |
| React | Component-based UI |
| PostgreSQL | Reliable relational database |
| SQLAlchemy | ORM support |
| Axios | Simple HTTP client |
| Ollama | Free local LLM |
| OpenAI | Cloud-based high-quality responses |
| Provider Factory | Easy extensibility |
| RAG | Context-aware responses |
| Markdown Artifacts | Easy copy, export, and rendering |

---

# 13. Security

- Backend stores API keys securely in `.env`
- No API keys exposed to the frontend
- Markdown rendering is sanitized
- CORS configured for frontend origin

---

# 14. Scalability

The architecture supports future enhancements such as:

- Vector databases
- Authentication
- Multi-user support
- Streaming responses
- Document uploads
- Semantic search
- Docker deployment
- CI/CD pipeline

---

# 15. Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | React + TypeScript |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| LLM Providers | Ollama, OpenAI |
| Knowledge Retrieval | RAG |
| HTTP Client | Axios |
| Markdown Rendering | React Markdown |
| Styling | CSS |
| Build Tool | Vite |

---

# Conclusion

The Lenny Growth Assistant follows a modular, layered architecture that cleanly separates the frontend, backend, AI orchestration, retrieval system, and provider abstraction. This structure improves maintainability, enables easy extension to new LLM providers or retrieval methods, and provides a scalable foundation for future enhancements.