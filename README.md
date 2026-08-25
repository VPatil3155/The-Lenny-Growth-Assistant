<div align="center">

# 🚀 The Lenny Growth Assistant

### AI-Powered Startup Growth Assistant with RAG, Multi-LLM Support & Artifact Generation

<p align="center">

<img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python">
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi">
<img src="https://img.shields.io/badge/React-19-61DAFB?logo=react">
<img src="https://img.shields.io/badge/TypeScript-5-blue?logo=typescript">
<img src="https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql">
<img src="https://img.shields.io/badge/Ollama-Local_LLM-black">
<img src="https://img.shields.io/badge/OpenAI-GPT-green">

</p>

**Generate startup strategies, marketing plans, emails, and growth insights using Retrieval-Augmented Generation (RAG) with interchangeable LLM providers.**

</div>

---

# 📸 Screenshots

> Replace these with your screenshots.

| Chat | Artifact Generation |
|------|---------------------|
| ![](docs/images/chat.png) | ![](docs/images/artifact.png) |

---

# ✨ Features

### 💬 AI Chat

- Multi-session conversations
- Automatic chat titles
- Rename & delete sessions
- Persistent chat history
- Markdown responses

---

### 📚 RAG Knowledge System

- Local knowledge base
- Markdown document loading
- Intelligent chunking
- Context retrieval
- Prompt enrichment

---

### 🤖 Multiple AI Providers

Switch instantly between

- Ollama (Local)
- OpenAI

without restarting the backend.

---

### 📄 Artifact Generation

Generate professional documents including

- Marketing Plans
- Growth Strategies
- Product Launch Plans
- Emails
- Meeting Summaries

---

### 🎨 Modern UI

- Responsive Design
- Markdown Rendering
- Copy Button
- Download as Markdown
- Clean Dashboard Layout

---

# 🏗 Architecture

```
                    React Frontend
                           │
                           ▼
                    FastAPI Backend
                           │
          ┌────────────────┼──────────────┐
          │                │              │
          ▼                ▼              ▼
     Chat Service     Artifact Service   Provider API
          │                │
          ▼                ▼
      RAG Engine      Prompt Templates
          │
          ▼
    Provider Factory
          │
     ┌────┴────┐
     ▼         ▼
 Ollama     OpenAI
```

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Frontend | React + TypeScript + Vite |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| AI | Ollama + OpenAI |
| Retrieval | RAG |
| Styling | CSS |
| Markdown | React Markdown |
| HTTP | Axios |

---

# 📂 Project Structure

```
The-Lenny-Growth-Assistant/

├── backend/
│   ├── api/
│   ├── app/
│   ├── models/
│   ├── rag/
│   ├── services/
│   ├── schemas/
│   ├── knowledge/
│   └── tests/
│
├── frontend/
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   ├── services/
│   └── types/
│
├── architecture.md
├── design.md
└── README.md
```

---

# 🚀 Quick Start

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/The-Lenny-Growth-Assistant.git

cd The-Lenny-Growth-Assistant
```

---

## 2. Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env

alembic upgrade head

uvicorn app.main:app --reload
```

Backend

```
http://127.0.0.1:8000
```

---

## 3. Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:5173
```

---

# ⚙ Environment Variables

```env
DATABASE_URL=

LLM_PROVIDER=ollama

OLLAMA_MODEL=llama3.2

OPENAI_API_KEY=

OPENAI_MODEL=gpt-4.1-mini
```

---

# 📖 API

Interactive Swagger Documentation

```
http://127.0.0.1:8000/docs
```

Main Endpoints

| Method | Endpoint |
|---------|----------|
| GET | /health |
| GET | /provider |
| POST | /provider |
| POST | /sessions |
| GET | /sessions |
| PATCH | /sessions/{id} |
| DELETE | /sessions/{id} |
| POST | /sessions/{id}/messages |
| GET | /sessions/{id}/messages |
| POST | /artifacts/generate |

---

# 📑 Documentation

Additional documentation is available in

- 📘 architecture.md
- 🎨 design.md

---

# 🔮 Future Improvements

- Authentication
- Vector Database
- Streaming Responses
- File Uploads
- Docker Deployment
- Kubernetes
- CI/CD Pipeline

---

# 🤝 Contributing

```bash
Fork

Create Feature Branch

Commit

Push

Open Pull Request
```

---

# 📄 License

MIT License

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a Star!

Made with ❤️ using React, FastAPI, PostgreSQL and AI.

</div>