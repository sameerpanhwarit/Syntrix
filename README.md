# 📚 Syntrix AI – FastAPI Backend

Syntrix AI is a smart AI-powered learning backend built using FastAPI. It allows users to upload books, ask AI questions from book content, and generate MCQ-based assessments using a Retrieval-Augmented Generation (RAG) system.

---

# 🚀 Features

- 🔐 JWT Authentication (Register/Login)
- 📚 Upload Books (PDF/Text)
- 🧠 AI Question Answering (RAG-based)
- 📖 Vector Search (Embeddings + FAISS)
- 🧩 MCQ Generation from Book Content
- 📊 MCQ Assessment with Scoring
- 🗄️ SQLite Database (upgradeable to PostgreSQL)
- ⚡ High-performance FastAPI backend

---

# 🏗️ Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- python-jose (JWT Auth)
- passlib (password hashing)
- HuggingFace embeddings
- FAISS (vector search)
- python-dotenv

---

# 📁 Project Structure
app/
│
├── api/              # All API routes
│   ├── auth.py
│   ├── upload.py
│   ├── qa.py
│   ├── mcq.py
│
├── core/             # Core logic
│   ├── auth.py       # JWT creation & verification
│   ├── config.py     # Environment variables
│   ├── deps.py       # Dependencies (get_current_user)
│
├── db/
│   ├── database.py   # DB connection
│
├── models/
│   ├── user.py
│   ├── book.py
│   ├── history.py
│
├── services/
│   ├── embeddings.py
│   ├── rag.py
│   ├── llm.py
│
├── utils/
│   ├── file_parser.py
│   ├── chunking.py
│
├── main.py

# ⚙️ Installation

## 1. Clone Repo
```bash
git clone https://github.com/your-repo/syntrix-ai.git
cd syntrix-ai
