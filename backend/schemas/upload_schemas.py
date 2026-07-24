"""Schemas for upload and dashboard responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Response payload for a successful upload."""

    filename: str
    path: str
    size: int
    uploaded_at: str


class DashboardResponse(BaseModel):
    """Response payload for dashboard metrics."""

    total_chats: int
    total_messages: int
    total_uploaded_files: int
    total_documents_in_vector_db: int
