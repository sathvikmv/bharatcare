"""Schemas for chat-related endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatCreateRequest(BaseModel):
    """Request body for creating a chat."""

    username: str = Field(..., min_length=1, max_length=100)
    title: Optional[str] = Field(default=None, max_length=255)


class MessageCreateRequest(BaseModel):
    """Request body for adding a message to an existing chat."""

    role: str = Field(..., min_length=1, max_length=20)
    content: str = Field(..., min_length=1)


class MessageOut(BaseModel):
    """Serialized message representation."""

    id: int
    role: str
    content: str
    timestamp: datetime


class ChatOut(BaseModel):
    """Serialized chat representation."""

    id: int
    user_id: int
    title: str
    created_at: datetime
    messages: List[MessageOut]
