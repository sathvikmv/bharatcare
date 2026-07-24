# AI Agent Backend Module (Member 3)

Backend module for the AI Agent project built with **FastAPI**, **SQLite (SQLAlchemy)**, **ChromaDB**, and **Sentence Transformers**.

## Components Implemented

1. **SQLite Database & Models**: `users`, `chats`, `messages` tables with automatic creation (`backend/database/`).
2. **Chat History APIs**:
   - `POST /chat/create`: Create a new chat session.
   - `GET /chat/list`: List all chat conversations.
   - `GET /chat/{id}`: Retrieve chat session details & message thread.
   - `POST /chat/{id}/message`: Append message to conversation.
   - `DELETE /chat/{id}`: Delete chat and cascading messages.
3. **File Upload & Processing**:
   - `POST /upload`: Uploads PDF, TXT, DOCX, CSV files into `backend/uploads/`.
   - File parsers extract textual content and automatically populate ChromaDB vector embeddings.
4. **Vector Database & RAG Search**:
   - `VectorService`: Document chunking and embedding storage via ChromaDB (`add_document`, `delete_document`, `search`).
   - `POST /rag/retrieve`: Returns top 5 context chunks for a user query (No LLM calls).
5. **Simple Memory**: `MemoryService` with `save_memory()`, `load_memory()`, `clear_memory()`.
6. **Dashboard API**:
   - `GET /dashboard`: Aggregated metrics (`total_chats`, `total_messages`, `total_uploaded_files`, `total_documents_in_vector_db`).
7. **Error Handling & Code Quality**: Clean modular structure, comprehensive docstrings, type hints, and standard HTTP error codes.

---

## How to Run

### 1. Environment Setup & Installation

Make sure your virtual environment is active and run:

```bash
pip install -r requirements.txt
```

### 2. Launch the FastAPI Server

Set `PYTHONPATH` to the root folder and start Uvicorn:

#### On Windows (PowerShell):
```powershell
$env:PYTHONPATH="c:\Users\Admin\full stack for vs code\AI-Chatbot"
cd backend
python -m uvicorn main:app --reload --port 8000
```

#### On Linux / macOS:
```bash
export PYTHONPATH="$(pwd)"
cd backend
python3 -m uvicorn main:app --reload --port 8000
```

### 3. Open API Documentation (Swagger UI)

Navigate to:
- **Interactive OpenAPI Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
