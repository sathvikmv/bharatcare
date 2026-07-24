"""Service layer for dashboard metrics."""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.database.models import Chat, Message, User
from backend.services.vector_service import VectorService


class DashboardService:
    """Collect dashboard statistics for the chatbot backend."""

    def __init__(self, db: Session, vector_service: VectorService | None = None) -> None:
        self.db = db
        self.vector_service = vector_service or VectorService()

    def get_metrics(self) -> dict:
        """Return aggregate counts for chats, messages, uploads, and vector data."""
        total_chats = self.db.query(Chat).count()
        total_messages = self.db.query(Message).count()
        total_users = self.db.query(User).count()
        total_uploaded_files = len(list(self.vector_service.collection.get()["ids"])) if hasattr(self.vector_service.collection, "get") else 0
        total_documents_in_vector_db = len(list(self.vector_service.collection.get()["ids"])) if hasattr(self.vector_service.collection, "get") else 0
        return {
            "total_chats": total_chats,
            "total_messages": total_messages,
            "total_uploaded_files": total_uploaded_files,
            "total_documents_in_vector_db": total_documents_in_vector_db,
        }
