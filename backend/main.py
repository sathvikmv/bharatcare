"""FastAPI application entrypoint for the chatbot backend module."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.connection import init_db
from backend.routers.chat_routes import router as chat_router
from backend.routers.dashboard_routes import router as dashboard_router
from backend.routers.rag_routes import router as rag_router
from backend.routers.upload_routes import router as upload_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Create the SQLite schema on startup."""
    init_db()
    yield


app = FastAPI(
    title="AI Agent Backend (Member 3)",
    version="1.0.0",
    description="FastAPI backend with ChromaDB RAG, SQLite chat history, and document ingestion.",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────────────────────
# Allow the Streamlit frontend (local or Render) to reach this API.
# Set ALLOWED_ORIGINS env var in Render to restrict to your domain.
_raw_origins = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:8501,http://127.0.0.1:8501,https://*.onrender.com,https://*.streamlit.app",
)
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.onrender\.com|https://.*\.streamlit\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(rag_router)
app.include_router(dashboard_router)


@app.get("/", tags=["health"])
def healthcheck() -> dict[str, str]:
    """Return a simple healthcheck payload."""
    return {"status": "ok", "message": "AI Agent backend (Member 3) is running"}
