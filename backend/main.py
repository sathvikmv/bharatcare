"""FastAPI application entrypoint for the chatbot backend module."""

from __future__ import annotations

from fastapi import FastAPI

from backend.database.connection import init_db
from backend.routers.chat_routes import router as chat_router
from backend.routers.dashboard_routes import router as dashboard_router
from backend.routers.rag_routes import router as rag_router
from backend.routers.upload_routes import router as upload_router

app = FastAPI(title="AI Agent Backend (Member 3)", version="1.0.0")

app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(rag_router)
app.include_router(dashboard_router)


@app.get("/")
def healthcheck() -> dict[str, str]:
    """Return a simple healthcheck payload."""
    return {"message": "AI Agent backend (Member 3) is running"}


@app.on_event("startup")
def startup_event() -> None:
    """Create the SQLite schema and initialize supporting folders."""
    init_db()

