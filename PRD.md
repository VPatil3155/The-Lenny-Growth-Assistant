# 📋 Product Requirements Document (PRD)

## 🎯 Goals

The Lenny Growth Assistant is designed to provide startup teams with an AI-powered workspace for growth planning, strategy generation, and contextual conversations.

The primary goals are:

- Build an AI-powered growth assistant for startup teams.
- Support persistent AI chat with contextual memory using Retrieval-Augmented Generation (RAG).
- Generate structured business artifacts such as marketing plans, emails, launch plans, and growth strategies.
- Support multiple LLM providers (Ollama and OpenAI) with runtime switching.

---

# Functional Requirements

## 💬 Chat

| ID | Requirement |
|----|-------------|
| CHAT-1 | Users can create new chat sessions. |
| CHAT-2 | Users can send messages and receive AI-generated responses. |
| CHAT-3 | Chat history is persisted in PostgreSQL. |
| CHAT-4 | Sessions are displayed in a sidebar sorted by newest first. |
| CHAT-5 | Users can rename sessions inline. |
| CHAT-6 | Users can delete sessions. |
| CHAT-7 | Session titles are automatically generated from the first message. |
| CHAT-8 | Assistant responses support Markdown rendering. |
| CHAT-9 | Typing indicator is displayed while waiting for responses. |
| CHAT-10 | Chat automatically scrolls to the latest message. |
| CHAT-11 | Press Enter to send and Shift+Enter for newline. |
| CHAT-12 | Input is disabled while waiting for the LLM. |

---

## 📚 Retrieval-Augmented Generation (RAG)

| ID | Requirement |
|----|-------------|
| RAG-1 | Load Markdown/Text documents from the local knowledge directory. |
| RAG-2 | Split documents into overlapping chunks (500 characters with 100 overlap). |
| RAG-3 | Retrieve the top three matching chunks using keyword search. |
| RAG-4 | Inject retrieved context into the LLM prompt before generation. |

---

## 📄 Artifact Generation

| ID | Requirement |
|----|-------------|
| ART-1 | Generate artifacts using a selected template. |
| ART-2 | Support Marketing Plans, Emails, Growth Strategies, Product Launch Plans, and Meeting Summaries. |
| ART-3 | Display generated artifacts in a slide-in panel. |
| ART-4 | Render Markdown with headings, tables, lists, and code blocks. |
| ART-5 | Sanitize embedded HTML before rendering. |
| ART-6 | Copy generated content to clipboard. |
| ART-7 | Download artifacts as Markdown files. |
| ART-8 | Display loading, error, and empty states. |
| ART-9 | Responsive layout for desktop and mobile devices. |

---

## 🤖 Provider Management

| ID | Requirement |
|----|-------------|
| PROV-1 | Switch between Ollama and OpenAI. |
| PROV-2 | Display provider availability status. |
| PROV-3 | Apply provider changes without restarting the backend. |
| PROV-4 | Persist selected provider in browser storage. |
| PROV-5 | Show descriptive messages when providers are unavailable. |

---

## ⚙️ Infrastructure

| ID | Requirement |
|----|-------------|
| INF-1 | FastAPI backend with OpenAPI documentation. |
| INF-2 | React + TypeScript single-page frontend. |
| INF-3 | CORS configured for local development. |
| INF-4 | PostgreSQL managed using Alembic migrations. |
| INF-5 | Database connectivity checked during startup. |
| INF-6 | Health endpoint available at `/health`. |

---